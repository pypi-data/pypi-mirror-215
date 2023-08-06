from typing import Any, Callable, Dict, Optional, Tuple, Type, Union
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import (
    Activation,
    BatchNormalization,
    Conv1D,
    Dense,
    Dropout,
    LayerNormalization,
    MaxPool1D,
    Input,
    Flatten,
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
    "n_encoder_layers": 1,
    "n_decoder_layers": 1,
    "attention_hidden_sizes": 32 * 1,
    "num_heads": 1,
    "attention_dropout": 0.0,
    "ffn_hidden_sizes": 32 * 1,
    "ffn_filter_sizes": 32 * 1,
    "ffn_dropout": 0.0,
    "skip_connect_circle": False,
    "skip_connect_mean": False,
}

class Encoder(tf.keras.layers.Layer):
    def __init__(self, layers, conv_layers=None, norm_layer=None) -> None:
        super(Encoder, self).__init__()
        self.layers = layers
        self.conv_layers = conv_layers if conv_layers is not None else None
        self.norm_layer = norm_layer

    def call(self, x, mask=None):
        """Informer encoder call function"""

        if self.conv_layers is not None:
            for attn_layer, conv_layer in zip(self.layers, self.conv_layers):
                x = attn_layer(x, mask)
                x = conv_layer(x)
            x = self.layers[-1](x, mask)

        else:
            for attn_layer in self.layers:
                x = attn_layer(x, mask)

        if self.norm_layer is not None:
            x = self.norm_layer(x)
        return x


class EncoderLayer(tf.keras.layers.Layer):
    def __init__(self, attention_hidden_sizes, num_heads, attention_dropout, ffn_hidden_sizes, ffn_dropout) -> None:
        super().__init__()
        self.attention_hidden_sizes = attention_hidden_sizes
        self.num_heads = num_heads
        self.attention_dropout = attention_dropout
        self.ffn_hidden_sizes = ffn_hidden_sizes
        self.ffn_dropout = ffn_dropout

    def build(self, input_shape):
        self.attn_layer = SelfAttention(self.attention_hidden_sizes, self.num_heads, self.attention_dropout)
        self.drop = Dropout(self.ffn_dropout)
        self.norm1 = LayerNormalization()
        self.conv1 = Conv1D(filters=self.ffn_hidden_sizes, kernel_size=1)
        self.conv2 = Conv1D(filters=self.attention_hidden_sizes, kernel_size=1)
        self.norm2 = LayerNormalization()
        super(EncoderLayer, self).build(input_shape)

    def call(self, x, mask=None):
        """Informer encoder layer call
        """
        input = x
        x = self.attn_layer(x, mask)
        x = self.drop(x)
        x = x + input

        y = x = self.norm1(x)
        y = self.conv1(y)
        y = self.drop(y)
        y = self.conv2(y)
        y = self.drop(y)
        y = x + y
        y = self.norm2(y)
        return y

    def get_config(self):
        config = {
            "attention_hidden_sizes": self.attention_hidden_sizes,
            "num_heads": self.num_heads,
            "attention_dropout": self.attention_dropout,
            "ffn_hidden_sizes": self.ffn_hidden_sizes,
            "ffn_dropout": self.ffn_dropout,
        }
        base_config = super(EncoderLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

class CustomConv(tf.keras.layers.Layer):
    def __init__(self, filters) -> None:
        super().__init__()
        self.filters = filters

    def build(self, input_shape):
        self.conv = Conv1D(filters=self.filters, kernel_size=3, padding="same")
        self.norm = BatchNormalization()
        self.activation = Activation("elu")
        self.pool = MaxPool1D(pool_size=3, strides=2, padding="same")
        super(CustomConv, self).build(input_shape)

    def call(self, x):
        """Informer custom conv
        """
        x = self.conv(x)
        x = self.norm(x)
        x = self.activation(x)
        x = self.pool(x)
        return x


class Decoder(tf.keras.layers.Layer):
    def __init__(self, layers, norm_layer=None):
        super().__init__()
        self.layers = layers
        self.norm = norm_layer

    def call(self, x, memory=None, x_mask=None, memory_mask=None):
        """Informer decoder call function
        """
        for layer in self.layers:
            x = layer(x, memory, x_mask, memory_mask)

        if self.norm is not None:
            x = self.norm(x)
        return x


class DecoderLayer(tf.keras.layers.Layer):
    def __init__(self, attention_hidden_sizes, num_heads, attention_dropout, ffn_hidden_sizes, ffn_dropout) -> None:
        super().__init__()
        self.attention_hidden_sizes = attention_hidden_sizes
        self.num_heads = num_heads
        self.attention_dropout = attention_dropout
        self.ffn_hidden_sizes = ffn_hidden_sizes
        self.ffn_dropout = ffn_dropout

    def build(self, input_shape):
        self.attn1 = SelfAttention(self.attention_hidden_sizes, self.num_heads, self.attention_dropout)
        self.attn2 = FullAttention(self.attention_hidden_sizes, self.num_heads, self.attention_dropout)
        self.conv1 = Conv1D(filters=self.ffn_hidden_sizes, kernel_size=1)
        self.conv2 = Conv1D(filters=self.attention_hidden_sizes, kernel_size=1)
        self.drop = Dropout(self.ffn_dropout)
        self.norm1 = LayerNormalization()
        self.norm2 = LayerNormalization()
        self.norm3 = LayerNormalization()
        self.activation = Activation("relu")
        super(DecoderLayer, self).build(input_shape)

    def call(self, x, memory=None, x_mask=None, memory_mask=None):
        """Informer decoder layer call function
        """
        x0 = x
        x = self.attn1(x, x_mask)
        x = self.drop(x)
        x = x + x0
        x = self.norm1(x)

        x1 = x
        x = self.attn2(x, memory, memory, mask=memory_mask)
        x = self.drop(x)
        x = x + x1
        x = self.norm2(x)

        x2 = x
        x = self.conv1(x)
        x = self.activation(x)
        x = self.drop(x)
        x = self.conv2(x)
        x = x + x2
        return self.norm3(x)

    def get_config(self):
        config = {
            "attention_hidden_sizes": self.attention_hidden_sizes,
            "num_heads": self.num_heads,
            "attention_dropout": self.attention_dropout,
            "ffn_hidden_sizes": self.ffn_hidden_sizes,
            "ffn_dropout": self.ffn_dropout,
        }
        base_config = super(DecoderLayer, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))
    
class Informer(object):
    """Informer model for time series"""

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
        self.predict_sequence_length = predict_sequence_length
        self.flatten=(Flatten())
        self.encoder_embedding = TokenEmbedding(params["attention_hidden_sizes"])
        self.decoder_embedding = TokenEmbedding(params["attention_hidden_sizes"])
        self.encoder = Encoder(
            layers=[
                EncoderLayer(
                    attention_hidden_sizes=params["attention_hidden_sizes"],
                    num_heads=params["num_heads"],
                    attention_dropout=params["attention_dropout"],
                    ffn_dropout=params["ffn_dropout"],
                    ffn_hidden_sizes=params["ffn_hidden_sizes"],
                )
                for _ in range(params["n_encoder_layers"])
            ],

            norm_layer=LayerNormalization(),
        )
        self.decoder = Decoder(
            layers=[
                DecoderLayer(
                    attention_hidden_sizes=params["attention_hidden_sizes"],
                    num_heads=params["num_heads"],
                    attention_dropout=params["attention_dropout"],
                    ffn_dropout=params["ffn_dropout"],
                    ffn_hidden_sizes=params["ffn_hidden_sizes"],
                )
                for _ in range(params["n_decoder_layers"])
            ]
        )
        self.projection = Dense(predict_sequence_length)

    def __call__(self, inputs, teacher=None):
        """Informer call fucntion
        """
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
                tf.reshape(tf.range(self.predict_sequence_length), (-1, self.predict_sequence_length, 1)), tf.float32
            )

        encoder_feature = self.encoder_embedding(encoder_feature)  # batch * seq * embedding_size
        memory = self.encoder(encoder_feature, mask=None)

        decoder_feature = self.decoder_embedding(decoder_feature)
        decoder_outputs = self.decoder(decoder_feature, memory=memory)
        decoder_outputs=self.flatten(decoder_outputs)
        decoder_outputs = self.projection(decoder_outputs)

        if self.params["skip_connect_circle"]:
            x_mean = x[:, -self.predict_sequence_length :, 0:1]
            decoder_outputs = decoder_outputs + x_mean
        if self.params["skip_connect_mean"]:
            x_mean = tf.tile(tf.reduce_mean(x[:, :, 0:1], axis=1, keepdims=True), [1, self.predict_sequence_length, 1])
            decoder_outputs = decoder_outputs + x_mean
        return decoder_outputs
    def getModel(self):

        inp = Input(shape=(self.n_steps,self.n_features))
        x = Informer(self.n_steps,self.n_features,self.predict_sequence_length)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model