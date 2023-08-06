from keras.layers import Layer
from keras import backend as K
import tensorflow as tf
from tensorflow.keras.layers import  Flatten, Dense, Input,BatchNormalization

class RBFLayer(Layer):
    def __init__(self, units, gamma, **kwargs):
        super(RBFLayer, self).__init__(**kwargs)
        self.units = units
        self.gamma = K.cast_to_floatx(gamma)

    def build(self, input_shape):
        self.mu = self.add_weight(name='mu',
                                  shape=(int(input_shape[1]), self.units),
                                  initializer='uniform',
                                  trainable=True)
        super(RBFLayer, self).build(input_shape)

    def call(self, inputs):
        diff = K.expand_dims(inputs) - self.mu
        l2 = K.sum(K.pow(diff,2), axis=1)
        res = K.exp(-1 * self.gamma * l2)
        return res

    def compute_output_shape(self, input_shape):
        return (input_shape[0], self.units)
    
class RBFN_Model(tf.keras.Model):
    def __init__(self, n_steps, n_features, n_outputs=1):
        super(RBFN_Model, self).__init__()
        self.n_steps = n_steps
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.Batch_1=BatchNormalization(input_shape = (n_steps, n_features))
        self.RBFN_RBFLayer=(RBFLayer(64,0.5))
        self.RBFN_RBFLayer2=(RBFLayer(64,0.5))
        self.RBFN_flatten=(Flatten())
        self.RBFN_flatten2=(Flatten())
        self.RBFN_dense1=(Dense(self.n_outputs, activation='sigmoid'))
        self.RBFN_RBFLayer3=(RBFLayer(self.n_outputs,0.5))

    def call(self, x):
        x=self.Batch_1(x)
        x = self.RBFN_flatten(x)
        x = self.RBFN_RBFLayer(x)
        x = self.RBFN_flatten(x)
        x = self.RBFN_RBFLayer2(x)
        x = self.RBFN_flatten2(x)
        x = self.RBFN_RBFLayer3(x)
        x = self.RBFN_dense1(x)

        return x
    
    def getModel(self):
        inp = Input(shape=(self.n_steps, self.n_features))
        x =  RBFN_Model(self.n_steps, self.n_features, self.n_outputs)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model

    