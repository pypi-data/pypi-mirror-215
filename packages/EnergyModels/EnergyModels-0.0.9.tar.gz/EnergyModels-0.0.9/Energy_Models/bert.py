import numpy as np 
import pandas as pd
import seaborn as sns
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import (
    GRU,
    AveragePooling1D,
    BatchNormalization,
    Dense,
    Dropout,
    LayerNormalization,
    SpatialDropout1D,
    Conv1D,
    Input,
    Flatten,
    LSTM,
    Embedding,
)

class FullAttention(tf.keras.layers.Layer):
    """Multi-head attention layer"""

    def __init__(self, hidden_size: int, num_heads: int, attention_dropout: float = 0.0):
        if hidden_size % num_heads:
            raise ValueError(
                "Hidden size ({}) must be divisible by the number of heads ({}).".format(hidden_size, num_heads)
            )
        super(FullAttention, self).__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.attention_dropout = attention_dropout

    def build(self, input_shape):
        self.dense_q = Dense(self.hidden_size, use_bias=False)
        self.dense_k = Dense(self.hidden_size, use_bias=False)
        self.dense_v = Dense(self.hidden_size, use_bias=False)
        self.dropout = Dropout(rate=self.attention_dropout)
        super(FullAttention, self).build(input_shape)

    def call(self, q, k, v, mask=None):
        q = self.dense_q(q)  # project the query/key/value to num_heads * units
        k = self.dense_k(k)
        v = self.dense_v(v)

        q_ = tf.concat(tf.split(q, self.num_heads, axis=2), axis=0)  # multi-heads transfer to
        k_ = tf.concat(tf.split(k, self.num_heads, axis=2), axis=0)
        v_ = tf.concat(tf.split(v, self.num_heads, axis=2), axis=0)

        score = tf.linalg.matmul(q_, k_, transpose_b=True)  # => (batch * heads) * seq_q * seq_k
        score /= tf.cast(tf.shape(q_)[-1], tf.float32) ** 0.5

        if mask is not None:
            score = score * tf.cast(mask, tf.float32)

        score = tf.nn.softmax(score)
        score = self.dropout(score)

        outputs = tf.linalg.matmul(score, v_)  # (batch * heads) * seq_q * units
        outputs = tf.concat(tf.split(outputs, self.num_heads, axis=0), axis=2)
        return outputs

    def get_config(self):
        config = {
            "hidden_size": self.hidden_size,
            "num_heads": self.num_heads,
            "attention_dropout": self.attention_dropout,
        }
        base_config = super(FullAttention, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class SelfAttention(tf.keras.layers.Layer):
    def __init__(self, hidden_size: int, num_heads: int, attention_dropout: float = 0.0):
        super(SelfAttention, self).__init__()
        self.attention = FullAttention(hidden_size, num_heads, attention_dropout=attention_dropout)

    def build(self, input_shape):
        super(SelfAttention, self).build(input_shape)

    def call(self, x, mask=None):
        return self.attention(x, x, x, mask)

    def get_config(self):
        base_config = super(SelfAttention, self).get_config()
        return base_config

class FeedForwardNetwork(tf.keras.layers.Layer):
    def __init__(self, hidden_size: int, filter_size: int, relu_dropout: float = 0.0):
        super(FeedForwardNetwork, self).__init__()
        self.hidden_size = hidden_size
        self.filter_size = filter_size
        self.relu_dropout = relu_dropout

    def build(self, input_shape):
        self.filter_dense_layer = Dense(self.filter_size, use_bias=True, activation="relu")
        self.output_dense_layer = Dense(self.hidden_size, use_bias=True)
        self.drop = Dropout(self.relu_dropout)
        super(FeedForwardNetwork, self).build(input_shape)

    def call(self, x):
        output = self.filter_dense_layer(x)
        output = self.drop(output)
        output = self.output_dense_layer(output)
        return output

    def get_config(self):
        config = {
            "hidden_size": self.hidden_size,
            "filter_size": self.filter_size,
            "relu_dropout": self.relu_dropout,
        }
        base_config = super(FeedForwardNetwork, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class TokenEmbedding(tf.keras.layers.Layer):
    """
    x: batch * time * feature
    outout: batch * time * new_attention_size）
    """

    def __init__(self, embed_size: int):
        super(TokenEmbedding, self).__init__()
        self.embed_size = embed_size

    def build(self, input_shape):
        self.token_weights = self.add_weight(
            name="token_weights",
            shape=[input_shape[-1], self.embed_size],
            initializer=tf.random_normal_initializer(mean=0.0, stddev=self.embed_size**-0.5),
        )
        super(TokenEmbedding, self).build(input_shape)

    def call(self, x):
        y = tf.einsum("bsf,fk->bsk", x, self.token_weights)
        return y

    def get_config(self):
        config = {"embed_size": self.embed_size}
        base_config = super(TokenEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class TokenRnnEmbedding(tf.keras.layers.Layer):
    def __init__(self, embed_size: int) -> None:
        super().__init__()
        self.embed_size = embed_size

    def build(self, input_shape):
        self.rnn = GRU(self.embed_size, return_sequences=True, return_state=True)
        super().build(input_shape)

    def call(self, x):
        y, _ = self.rnn(x)
        return y

    def get_config(self):
        config = {"embed_size": self.embed_size}
        base_config = super(TokenRnnEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class PositionalEmbedding(tf.keras.layers.Layer):
    def __init__(self, max_len: int = 5000):
        super(PositionalEmbedding, self).__init__()
        self.max_len = max_len

    def build(self, input_shape):
        super(PositionalEmbedding, self).build(input_shape)

    def call(self, x, masking=True):

        E = x.get_shape().as_list()[-1]  # static
        batch_size, seq_length = tf.shape(x)[0], tf.shape(x)[1]  # dynamic

        position_ind = tf.tile(tf.expand_dims(tf.range(seq_length), 0), [batch_size, 1])  # => batch_size * seq_length
        position_enc = np.array(
            [[pos / np.power(10000, (i - i % 2) / E) for i in range(E)] for pos in range(self.max_len)]
        )

        position_enc[:, 0::2] = np.sin(position_enc[:, 0::2])
        position_enc[:, 1::2] = np.cos(position_enc[:, 1::2])
        position_enc = tf.convert_to_tensor(position_enc, tf.float32)  # (maxlen, E)

        outputs = tf.nn.embedding_lookup(position_enc, position_ind)
        if masking:
            outputs = tf.where(tf.equal(x, 0), x, outputs)
        return tf.cast(outputs, tf.float32)

    def get_config(self):
        config = {"max_len": self.max_len}
        base_config = super(PositionalEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


class PositionalEncoding(tf.keras.layers.Layer):
    def __init__(self, max_len: int = 5000):
        super(PositionalEncoding, self).__init__()
        self.max_len = max_len

    def build(self, input_shape):
        super(PositionalEncoding, self).build(input_shape)

    def call(self, x, masking=True):

        E = x.get_shape().as_list()[-1]  # static
        batch_size, seq_length = tf.shape(x)[0], tf.shape(x)[1]  # dynamic
        with tf.name_scope("position_encode"):
            # # => batch_size * seq_length
            position_ind = tf.tile(tf.expand_dims(tf.range(seq_length), 0), [batch_size, 1])
            position_enc = np.array(
                [[pos / np.power(10000, (i - i % 2) / E) for i in range(E)] for pos in range(self.max_len)]
            )

            position_enc[:, 0::2] = np.sin(position_enc[:, 0::2])
            position_enc[:, 1::2] = np.cos(position_enc[:, 1::2])
            position_enc = tf.convert_to_tensor(position_enc, tf.float32)  # (maxlen, E)

            outputs = tf.nn.embedding_lookup(position_enc, position_ind)
            if masking:
                outputs = tf.where(tf.equal(x, 0), x, outputs)
        return tf.cast(outputs, tf.float32)

    def get_config(self):
        config = {"max_len": self.max_len}
        base_config = super(PositionalEncoding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    
class DataEmbedding(tf.keras.layers.Layer):
    def __init__(self, embed_size: int, dropout: float = 0.0):
        super(DataEmbedding, self).__init__()
        self.embed_size = embed_size
        self.value_embedding = TokenEmbedding(embed_size)
        self.positional_embedding = PositionalEncoding()
        self.dropout = Dropout(dropout)

    def build(self, input_shape):
        super(DataEmbedding, self).build(input_shape)

    def call(self, x):

        ve = self.value_embedding(x)
        pe = self.positional_embedding(ve)
        return self.dropout(ve + pe)

    def get_config(self):
        config = {"embed_size": self.embed_size}
        base_config = super(DataEmbedding, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
    

class Encoder(tf.keras.layers.Layer):
    def __init__(
        self,
        n_encoder_layers,
        attention_hidden_sizes,
        num_heads,
        attention_dropout,
        ffn_hidden_sizes,
        ffn_filter_sizes,
        ffn_dropout,
    ):
        super(Encoder, self).__init__()
        self.n_encoder_layers = n_encoder_layers
        self.attention_hidden_sizes = attention_hidden_sizes
        self.num_heads = num_heads
        self.attention_dropout = attention_dropout
        self.ffn_hidden_sizes = ffn_hidden_sizes
        self.ffn_filter_sizes = ffn_filter_sizes
        self.ffn_dropout = ffn_dropout
        self.layers = []

    def build(self, input_shape):
        for _ in range(self.n_encoder_layers):
            attention_layer = SelfAttention(self.attention_hidden_sizes, self.num_heads, self.attention_dropout)
            feed_forward_layer = FeedForwardNetwork(self.ffn_hidden_sizes, self.ffn_filter_sizes, self.ffn_dropout)
            ln_layer1 = LayerNormalization(epsilon=1e-6, dtype="float32")
            ln_layer2 = LayerNormalization(epsilon=1e-6, dtype="float32")
            self.layers.append([attention_layer, ln_layer1, feed_forward_layer, ln_layer2])
        super(Encoder, self).build(input_shape)

    def call(self, encoder_inputs, src_mask=None):

        x = encoder_inputs
        for _, layer in enumerate(self.layers):
            attention_layer, ln_layer1, ffn_layer, ln_layer2 = layer
            enc = x
            enc = attention_layer(enc, src_mask)
            enc1 = ln_layer1(x + enc)  # residual connect
            enc1 = ffn_layer(enc1)
            x = ln_layer2(enc + enc1)
        return x

    def get_config(self):
        config = {
            "n_encoder_layers": self.n_encoder_layers,
            "attention_hidden_sizes": self.attention_hidden_sizes,
            "num_heads": self.num_heads,
            "attention_dropout": self.attention_dropout,
            "ffn_hidden_sizes": self.ffn_hidden_sizes,
            "ffn_filter_sizes": self.ffn_filter_sizes,
            "ffn_dropout": self.ffn_dropout,
        }
        base_config = super(Encoder, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))


params = {
    "n_encoder_layers": 1,
    "use_token_embedding": False,
    "attention_hidden_sizes": 32 * 1,
    "num_heads": 2,
    "attention_dropout": 0.0,
    "ffn_hidden_sizes": 32 * 1,
    "ffn_filter_sizes": 32 * 1,
    "ffn_dropout": 0.0,
    "layer_postprocess_dropout": 0.0,
    "scheduler_sampling": 1,  # 0 means teacher forcing, 1 means use last prediction
    "skip_connect_circle": False,
    "skip_connect_mean": False,
}


class Bert(object):
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
        self.n_steps=n_steps
        self.n_features=n_features
        self.flatten=(Flatten())
        self.predict_sequence_length = predict_sequence_length
        self.encoder_embedding = TokenEmbedding(params["attention_hidden_sizes"])
        self.encoder = Encoder(
            params["n_encoder_layers"],
            params["attention_hidden_sizes"],
            params["num_heads"],
            params["attention_dropout"],
            params["ffn_hidden_sizes"],
            params["ffn_filter_sizes"],
            params["ffn_dropout"],
        )

        self.project1 = Dense(predict_sequence_length, activation="sigmoid")
        # self.project1 = Dense(48, activation=None)

        self.drop1 = Dropout(0.25)
        self.dense1 = Dense(512, activation="relu")

        self.drop2 = Dropout(0.25)
        self.dense2 = Dense(1024, activation="relu")


    def __call__(self, inputs, teacher=None):

        if isinstance(inputs, (list, tuple)):
            x, encoder_feature, decoder_feature = inputs
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        elif isinstance(inputs, dict):
            x = inputs["x"]
            encoder_feature = inputs["encoder_feature"]
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        else:
            encoder_feature = x = inputs

        encoder_feature = self.encoder_embedding(encoder_feature)

        memory = self.encoder(encoder_feature, src_mask=None)  # batch * train_sequence * (hidden * heads)
        encoder_output = memory[:, -1]

        encoder_output = self.drop1(encoder_output)
        encoder_output = self.dense1(encoder_output)
        encoder_output = self.drop2(encoder_output)
        encoder_output = self.dense2(encoder_output)
        encoder_output = self.drop2(encoder_output)

        outputs = self.project1(encoder_output)


        if self.params["skip_connect_circle"]:
            x_mean = x[:, -self.predict_sequence_length :, :]
            outputs = outputs + x_mean
        if self.params["skip_connect_mean"]:
            x_mean = tf.tile(tf.reduce_mean(x, axis=1, keepdims=True), [1, self.predict_sequence_length, 1])
            outputs = outputs + x_mean
        return outputs
    
    def getModel(self):
        inp = Input(shape=(self.n_steps,self.n_features))
        x = Bert(self.n_steps,self.n_features,self.predict_sequence_length)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model

