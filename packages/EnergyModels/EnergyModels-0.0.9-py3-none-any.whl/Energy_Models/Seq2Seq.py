import warnings
warnings.filterwarnings('ignore')
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import GRU, LSTM, Dense, Dropout, GRUCell, LSTMCell ,Input,Flatten


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
        """use query and key generating an attention multiplier for value, multi_heads to repeat it
        Parameters
        ----------
        q : _type_
            Query with shape batch * seq_q * fea
        k : _type_
            Key with shape batch * seq_k * fea
        v : _type_
            value with shape batch * seq_v * fea
        mask : _type_, optional
            important to avoid the leaks, defaults to None, by default None
        Returns
        -------
        _type_
            tensor with shape batch * seq_q * (units * num_heads)
        """
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

params = {
    "rnn_type": "gru",
    "bi_direction": False,
    "rnn_size": 64,
    "dense_size": 64,
    "num_stacked_layers": 1,
    "scheduler_sampling": 0,  # teacher forcing
    "use_attention": False,
    "attention_sizes": 64,
    "attention_heads": 2,
    "attention_dropout": 0,
    "skip_connect_circle": False,
    "skip_connect_mean": False,
}


class Encoder(tf.keras.layers.Layer):
    def __init__(self, rnn_type, rnn_size, rnn_dropout=0, dense_size=32, **kwargs):
        super(Encoder, self).__init__(**kwargs)
        if rnn_type.lower() == "gru":
            self.rnn = GRU(
                units=rnn_size, activation="tanh", return_state=True, return_sequences=True, dropout=rnn_dropout
            )
        elif self.rnn_type.lower() == "lstm":
            self.rnn = LSTM(
                units=self.rnn_size,
                activation="tanh",
                return_state=True,
                return_sequences=True,
                dropout=self.rnn_dropout,
            )
        self.dense = Dense(units=dense_size, activation="tanh")

    def call(self, inputs):

        outputs, state = self.rnn(inputs)
        state = self.dense(state)
        return outputs, state


class Decoder1(tf.keras.layers.Layer):
    def __init__(
        self,
        rnn_type="gru",
        rnn_size=32,
        predict_sequence_length=3,
        use_attention=False,
        attention_sizes=32,
        attention_heads=1,
        attention_dropout=0.0,
    ):
        super(Decoder1, self).__init__()
        self.predict_sequence_length = predict_sequence_length
        self.use_attention = use_attention
        self.rnn_type = rnn_type
        self.rnn_size = rnn_size
        self.attention_sizes = attention_sizes
        self.attention_heads = attention_heads
        self.attention_dropout = attention_dropout

    def build(self, input_shape):
        if self.rnn_type.lower() == "gru":
            self.rnn_cell = GRUCell(self.rnn_size)
        elif self.rnn_type.lower() == "lstm":
            self.rnn = LSTMCell(units=self.rnn_size)
        self.dense = Dense(units=1, activation=None)
        if self.use_attention:
            self.attention = FullAttention(
                hidden_size=self.attention_sizes,
                num_heads=self.attention_heads,
                attention_dropout=self.attention_dropout,
            )

    def call(
        self,
        decoder_features,
        decoder_init_input,
        init_state,
        teacher=None,
        scheduler_sampling=0,
        training=None,
        **kwargs
    ):

        decoder_outputs = []
        prev_output = decoder_init_input
        prev_state = init_state
        if teacher is not None:
            teacher = tf.squeeze(teacher, 2)
            teachers = tf.split(teacher, self.predict_sequence_length, axis=1)

        for i in range(self.predict_sequence_length):
            if training:
                p = np.random.uniform(low=0, high=1, size=1)[0]
                if teacher is not None and p > scheduler_sampling:
                    this_input = teachers[i]
                else:
                    this_input = prev_output
            else:
                this_input = prev_output

            if decoder_features is not None:
                this_input = tf.concat([this_input, decoder_features[:, i]], axis=-1)

            if self.use_attention:
                att = self.attention(
                    tf.expand_dims(prev_state, 1), k=kwargs["encoder_output"], v=kwargs["encoder_output"]
                )
                att = tf.squeeze(att, 1)
                this_input = tf.concat([this_input, att], axis=-1)

            this_output, this_state = self.rnn_cell(this_input, prev_state)
            prev_state = this_state
            prev_output = self.dense(this_output)
            decoder_outputs.append(prev_output)

        decoder_outputs = tf.concat(decoder_outputs, axis=-1)
        return tf.expand_dims(decoder_outputs, -1)


class Decoder2(tf.keras.layers.Layer):
    def __init__(
        self,
        rnn_type="gru",
        rnn_size=32,
        predict_sequence_length=3,
        use_attention=False,
        attention_sizes=32,
        attention_heads=1,
        attention_dropout=0.0,
    ):
        super(Decoder2, self).__init__()
        self.rnn_type = rnn_type
        self.rnn_size = rnn_size
        self.predict_sequence_length = predict_sequence_length
        self.use_attention = use_attention
        self.attention_sizes = attention_sizes
        self.attention_heads = attention_heads
        self.attention_dropout = attention_dropout

    def build(self, input_shape):
        if self.rnn_type.lower() == "gru":
            self.rnn_cell = GRUCell(self.rnn_size)
        elif self.rnn_type.lower() == "lstm":
            self.rnn = LSTMCell(units=self.rnn_size)
        self.dense = Dense(units=1)
        if self.use_attention:
            self.attention = FullAttention(
                hidden_size=self.attention_sizes,
                num_heads=self.attention_heads,
                attention_dropout=self.attention_dropout,
            )

    def forward(
        self,
        decoder_feature,
        decoder_init_value,
        init_state,
        teacher=None,
        scheduler_sampling=0,
        training=None,
        **kwargs
    ):
        def cond_fn(time, prev_output, prev_state, decoder_output_ta):
            return time < self.predict_sequence_length

        def body(time, prev_output, prev_state, decoder_output_ta):
            if time == 0 or teacher is None:
                this_input = prev_output

            else:
                this_input = teacher[:, time - 1, :]

            if decoder_feature is not None:
                this_feature = decoder_feature[:, time, :]
                this_input = tf.concat([this_input, this_feature], axis=1)

            if self.use_attention:
                attention_feature = self.attention(
                    tf.expand_dims(prev_state[-1], 1), k=kwargs["encoder_output"], v=kwargs["encoder_output"]
                )
                attention_feature = tf.squeeze(attention_feature, 1)
                this_input = tf.concat([this_input, attention_feature], axis=-1)

            this_output, this_state = self.rnn_cell(this_input, prev_state)
            project_output = self.dense(this_output)
            decoder_output_ta = decoder_output_ta.write(time, project_output)
            return time + 1, project_output, this_state, decoder_output_ta

        loop_init = [
            tf.constant(0, dtype=tf.int32),  # steps
            decoder_init_value,  # decoder each step
            init_state,  # state
            tf.TensorArray(dtype=tf.float32, size=self.predict_sequence_length),
        ]
        _, _, _, decoder_outputs_ta = tf.while_loop(cond_fn, body, loop_init)

        decoder_outputs = decoder_outputs_ta.stack()
        decoder_outputs = tf.transpose(decoder_outputs, [1, 0, 2])
        return decoder_outputs

    def call(
        self,
        decoder_feature,
        decoder_init_input,
        init_state,
        teacher=None,
        scheduler_sampling=0,
        training=None,
        **kwargs
    ):

        return self.forward(
            decoder_feature=decoder_feature,
            decoder_init_value=decoder_init_input,
            init_state=[init_state],  # for tf2
            teacher=teacher,
        )


class Decoder3(tf.keras.layers.Layer):
    # multi-steps static decoding
    def __init__(self, rnn_type="gru", rnn_size=32, rnn_dropout=0, dense_size=1, **kwargs) -> None:
        super(Decoder3, self).__init__()
        if rnn_type.lower() == "gru":
            self.rnn = GRU(
                units=rnn_size, activation="tanh", return_state=False, return_sequences=True, dropout=rnn_dropout
            )
        elif rnn_type.lower() == "lstm":
            self.rnn = LSTM(
                units=rnn_size,
                activation="tanh",
                return_state=False,
                return_sequences=True,
                dropout=rnn_dropout,
            )
        self.dense = Dense(units=dense_size, activation=None)
        self.drop = Dropout(0.1)

    def call(
        self,
        decoder_features,
        decoder_init_input,
        init_state,
        teacher=None,
        scheduler_sampling=0,
        training=None,
        **kwargs
    ):

        x = self.rnn(decoder_features, initial_state=init_state)
        x = self.dense(x)
        return x


class Seq2Seq(object):
    """Seq2seq model"""

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
        self.encoder = Encoder(
            rnn_type=params["rnn_type"], rnn_size=params["rnn_size"], dense_size=params["dense_size"]
        )
        self.decoder = Decoder1(
            rnn_type=params["rnn_type"],
            rnn_size=params["rnn_size"],
            predict_sequence_length=predict_sequence_length,
            use_attention=params["use_attention"],
            attention_sizes=params["attention_sizes"],
            attention_heads=params["attention_heads"],
            attention_dropout=params["attention_dropout"],
        )
        self.projection = Dense(predict_sequence_length)

    def __call__(self, inputs, teacher=None):

        if isinstance(inputs, (list, tuple)):
            x, encoder_feature, decoder_feature = inputs
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        elif isinstance(inputs, dict):
            x = inputs["x"]
            encoder_feature = inputs["encoder_feature"]
            decoder_feature = inputs["decoder_feature"]
            encoder_feature = tf.concat([x, encoder_feature], axis=-1)
        else:
            encoder_feature = x = inputs
            decoder_feature = tf.cast(
                tf.tile(
                    tf.reshape(tf.range(self.predict_sequence_length), (1, self.predict_sequence_length, 1)),
                    (tf.shape(encoder_feature)[0], 1, 1),
                ),
                tf.float32,
            )

        encoder_outputs, encoder_state = self.encoder(encoder_feature)

        decoder_outputs = self.decoder(
            decoder_feature,
            decoder_init_input=x[:, -1, 0:1],
            init_state=encoder_state,
            teacher=teacher,
            scheduler_sampling=self.params["scheduler_sampling"],
            encoder_output=encoder_outputs,
        )
        
        decoder_outputs =self.flatten(decoder_outputs)
        decoder_outputs = self.projection(decoder_outputs)

        if self.params["skip_connect_circle"]:
            x_mean = x[:, : self.predict_sequence_length, :]
            decoder_outputs = decoder_outputs + x_mean
        if self.params["skip_connect_mean"]:
            x_mean = tf.tile(tf.reduce_mean(x, axis=1, keepdims=True), [1, self.predict_sequence_length, 1])
            decoder_outputs = decoder_outputs + x_mean
        return decoder_outputs

    def getModel(self):

        inp = Input(shape=(self.n_steps,self.n_features))
        x = Seq2Seq(self.n_steps,self.n_features,self.predict_sequence_length)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model


