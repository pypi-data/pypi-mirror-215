from typing import Any, Callable, Dict, Optional, Tuple, Type
import math
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Conv1D, Dense, Dropout, LayerNormalization, ReLU ,AveragePooling1D,Input


params = {
    "n_encoder_layers": 1,
    "n_decoder_layers": 1,
    "kernel_size": 24,
    "attention_hidden_sizes": 32,
    "num_heads": 1,
    "attention_dropout": 0.0,
    "ffn_hidden_sizes": 32 * 1,
    "ffn_filter_sizes": 32 * 1,
    "ffn_dropout": 0.0,
    "layer_postprocess_dropout": 0.0,
    "scheduler_sampling": 1,  # 0 means teacher forcing, 1 means use last prediction
    "skip_connect_circle": False,
    "skip_connect_mean": False,
}

class SeriesDecomp(tf.keras.layers.Layer):
    def __init__(self, kernel_size: int) -> None:
        super().__init__()
        self.kernel_size = kernel_size
        self.moving_avg = AveragePooling1D(pool_size=kernel_size, strides=1, padding="same")

    def call(self, x):

        x_ma = self.moving_avg(x)
        return x - x_ma, x_ma

    def get_config(self):
        config = {
            "kernel_size": self.kernel_size,
        }
        base_config = super().get_config()
        return dict(list(base_config.items()) + list(config.items()))


class AutoCorrelation(tf.keras.layers.Layer):

    def __init__(self, d_model: int, num_heads: int, attention_dropout: float = 0.0) -> None:
        super().__init__()
        self.d_model = d_model
        self.num_heads = num_heads
        self.depth = d_model // num_heads
        self.attention_dropout = attention_dropout

    def build(self, input_shape):
        self.wq = Dense(self.d_model, name="q")
        self.wk = Dense(self.d_model, name="k")
        self.wv = Dense(self.d_model, name="v")
        self.drop = Dropout(self.attention_dropout)
        self.dense = Dense(self.d_model, name="project")

    def time_delay_agg(self, q, k, v):  # TODO: v not used in process
        batch_size = tf.shape(q)[0]
        time_steps = tf.shape(q)[2]
        q_fft = tf.signal.rfft(tf.transpose(q, perm=[0, 1, 3, 2]))
        k_fft = tf.signal.rfft(tf.transpose(k, perm=[0, 1, 3, 2]))
        S_qk = q_fft * tf.math.conj(k_fft)
        R_qk = tf.signal.irfft(S_qk)

        init_index = tf.reshape(tf.range(time_steps), (1, 1, 1, -1))
        init_index = tf.tile(init_index, [batch_size, self.num_heads, self.depth, 1])
        top_k = int(2 * tf.math.log(tf.cast(time_steps, tf.float32)))
        weights, indices = tf.math.top_k(R_qk, top_k)

        tmp_corr = tf.nn.softmax(weights, axis=-1)

        tmp_values = tf.tile(tf.transpose(q, perm=[0, 1, 3, 2]), tf.constant([1, 1, 1, 2]))
        delays_agg = tf.zeros_like(tf.transpose(q, perm=[0, 1, 3, 2]))

        for i in range(top_k):
            pattern = tf.gather(tmp_values, init_index + tf.expand_dims(indices[..., i], -1), axis=-1, batch_dims=-1)
            delays_agg = delays_agg + pattern * (tf.expand_dims(tmp_corr[..., i], axis=-1))
        return delays_agg

    def split_heads(self, x, batch_size):
        x = tf.reshape(x, (batch_size, -1, self.num_heads, self.depth))
        return tf.transpose(x, perm=[0, 2, 1, 3])  # (batch_size, num_heads, timesteps, depth)

    def call(self, q, k, v, dynamic=True):

        batch_size = tf.shape(q)[0]

        q = self.drop(self.wq(q))
        k = self.drop(self.wk(k))
        v = self.drop(self.wv(v))

        q = self.split_heads(q, batch_size)
        k = self.split_heads(k, batch_size)
        v = self.split_heads(v, batch_size)

        L = tf.shape(q)[2]
        S = tf.shape(v)[2]

        if tf.math.greater(L, S):
            zeros = tf.zeros_like(q[:, :, : (L - S), :])
            v = tf.concat([v, zeros], axis=2)
            k = tf.concat([k, zeros], axis=2)
        else:
            v = v[:, :, :L, :]
            k = k[:, :, :L, :]

        delays_agg = self.time_delay_agg(q, k, v)
        delays_agg = tf.transpose(delays_agg, [0, 3, 1, 2])
        concat_delays_agg = tf.reshape(delays_agg, (batch_size, -1, self.d_model))
        output = self.dense(concat_delays_agg)
        return output

class EncoderLayer(tf.keras.layers.Layer):
    def __init__(self, kernel_size, d_model, num_heads, dropout_rate=0.1) -> None:
        super().__init__()
        self.series_decomp1 = SeriesDecomp(kernel_size)
        self.series_decomp2 = SeriesDecomp(kernel_size)
        self.autocorrelation = AutoCorrelation(d_model, num_heads)
        self.drop = Dropout(dropout_rate)

    def build(self, input_shape):
        self.dense = Dense(input_shape[-1])

    def call(self, x):
        x, _ = self.series_decomp2(self.drop(self.dense(x)) + x)
        return x


class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, kernel_size, d_model, num_heads, drop_rate=0.1) -> None:
        super().__init__()
        self.d_model = d_model
        self.drop_rate = drop_rate
        self.series_decomp1 = SeriesDecomp(kernel_size)
        self.series_decomp2 = SeriesDecomp(kernel_size)
        self.series_decomp3 = SeriesDecomp(kernel_size)
        self.autocorrelation1 = AutoCorrelation(d_model, num_heads)
        self.autocorrelation2 = AutoCorrelation(d_model, num_heads)

    def build(self, input_shape):
        self.conv1 = Conv1D(self.d_model, kernel_size=3, strides=1, padding="same")
        self.project = Conv1D(1, kernel_size=3, strides=1, padding="same")
        self.drop = Dropout(self.drop_rate)
        self.dense1 = Dense(input_shape[-1])
        self.conv2 = Conv1D(input_shape[-1], kernel_size=3, strides=1, padding="same")
        self.activation = ReLU()

    def call(self, x, cross, init_trend):

        x, trend1 = self.series_decomp1(self.drop(self.autocorrelation1(x, x, x)) + x)
        x, trend2 = self.series_decomp2(self.drop(self.autocorrelation2(x, cross, cross)) + x)
        x = self.conv2(self.drop(self.activation(self.conv1(x))))
        x, trend3 = self.series_decomp3(self.drop(self.dense1(x)) + x)

        trend = trend1 + trend2 + trend3
        trend = self.drop(self.project(trend))
        return x, init_trend + trend

class AutoFormer(object):
    def __init__(
        self,
        n_steps,
        n_features,
        predict_sequence_length,
        custom_model_params: Optional[Dict[str, Any]] = None,
        custom_model_head: Optional[Callable] = None,
    ):
        if custom_model_params:
            params.update(custom_model_params)
        self.params = params
        self.predict_sequence_length = predict_sequence_length
        self.n_steps=n_steps
        self.n_features=n_features

        self.series_decomp = SeriesDecomp(params["kernel_size"])
        self.encoder = [
            EncoderLayer(
                params["kernel_size"],
                params["attention_hidden_sizes"],
                params["num_heads"],
                params["attention_dropout"],
            )
            for _ in range(params["n_encoder_layers"])
        ]

        self.decoder = [
            DecoderLayer(
                params["kernel_size"],
                params["attention_hidden_sizes"],
                params["num_heads"],
                params["attention_dropout"],
            )
            for _ in range(params["n_decoder_layers"])
        ]

        self.project = Conv1D(1, kernel_size=3, strides=1, padding="same", use_bias=False)
        self.project1 = Dense(predict_sequence_length, activation="sigmoid")
        self.drop1 = Dropout(0.25)
        self.dense1 = Dense(512, activation="relu")
        self.drop2 = Dropout(0.25)
        self.dense2 = Dense(1024, activation="relu")
        self.dense3 = Dense(512, activation="relu")


    def __call__(self, inputs, teacher=None, **kwargs):

        if isinstance(inputs, (list, tuple)):
            x, encoder_feature, decoder_feature = inputs
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        elif isinstance(inputs, dict):
            x = inputs["x"]
            encoder_feature = inputs["encoder_feature"]
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        else:
            encoder_feature = x = inputs

        batch_size, _, n_feature = tf.shape(encoder_feature)
        # encoder
        for layer in self.encoder:
            x = layer(x)

        encoder_output = x[:, -1]
        encoder_output = self.drop1(encoder_output)
        encoder_output = self.dense1(encoder_output)
        encoder_output = self.drop2(encoder_output)
        encoder_output = self.dense2(encoder_output)
        encoder_output = self.drop2(encoder_output)
        encoder_output = self.dense3(encoder_output)
        outputs = self.project1(encoder_output)
        outputs = tf.expand_dims(outputs, -1)
        return outputs
    
    def getModel(self):

        inp = Input(shape=(self.n_steps,self.n_features))
        x = AutoFormer(self.n_steps,self.n_features,self.predict_sequence_length)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model


       