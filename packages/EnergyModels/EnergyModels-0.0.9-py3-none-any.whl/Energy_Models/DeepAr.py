from typing import Any, Callable, Dict, Optional, Tuple, Type
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Activation, BatchNormalization, Dense, Dropout,Conv1D,Input,Flatten


class GaussianLayer(tf.keras.layers.Layer):
    def __init__(self, units: int):
        self.units = units
        super(GaussianLayer, self).__init__()

    def build(self, input_shape):
        in_channels = input_shape[2]
        self.weight1 = self.add_weight(
            name="gauss_w1", shape=(in_channels, self.units), initializer=tf.keras.initializers.GlorotNormal()
        )
        self.weight2 = self.add_weight(
            name="gauss_w2", shape=(in_channels, self.units), initializer=tf.keras.initializers.GlorotNormal()
        )
        self.bias1 = self.add_weight(name="gauss_b1", shape=(self.units,), initializer=tf.keras.initializers.Zeros())
        self.bias2 = self.add_weight(name="gauss_b2", shape=(self.units,), initializer=tf.keras.initializers.Zeros())
        super(GaussianLayer, self).build(input_shape)

    def call(self, x):
        
        mu = tf.matmul(x, self.weight1) + self.bias1
        sig = tf.matmul(x, self.weight2) + self.bias2
        sig_pos = tf.math.log1p(tf.math.exp(sig)) + 1e-7
        return mu, sig_pos

    def get_config(self):
        return
    
params = {
    "rnn_size": 64,
    "skip_connect_circle": False,
    "skip_connect_mean": False,
}

class DeepAR(object):
    def __init__(
        self,
        n_steps,
        n_features,
        predict_sequence_length,
        custom_model_params: Optional[Dict[str, Any]] = None,
        custom_model_head: Optional[Callable] = None,
    ):
        """DeepAR Network
        :param custom_model_params:
        """
        if custom_model_params:
            params.update(custom_model_params)
        self.params = params
        self.predict_sequence_length = predict_sequence_length
        self.n_steps=n_steps
        self.n_features=n_features
        cell = tf.keras.layers.GRUCell(units=self.params["rnn_size"])
        self.rnn = tf.keras.layers.RNN(cell, return_state=True, return_sequences=True)
        self.bn = BatchNormalization()
        self.dense = Dense(units=32, activation="relu")
        self.gauss = GaussianLayer(units=predict_sequence_length)
        self.flatten=(Flatten())
        self.dense1 = Dense(units=predict_sequence_length, activation="linear")


    def __call__(self, x):

        x, _ = self.rnn(x)
        x = self.dense(x)
        loc, scale = self.gauss(x)
        scale =self.flatten(scale)
        scale = self.dense1(scale)
        return scale
    
    def getModel(self):
        inp = Input(shape=(self.n_steps,self.n_features))
        x = DeepAR(self.n_steps,self.n_features,self.predict_sequence_length)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model