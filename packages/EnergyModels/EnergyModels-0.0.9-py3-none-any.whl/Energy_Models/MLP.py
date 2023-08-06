import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input,Dense, Activation, Dropout,Flatten


class MLP(tf.keras.Model):
    def __init__(self,n_steps,n_features, n_outputs=1):
        super(MLP, self).__init__()
        self.n_steps=n_steps
        self.n_features = n_features
        self.n_outputs = n_outputs
        
        self.dense_1 = Dense(64, activation='relu')
        self.dropout_1 = Dropout(0.2)
        self.flatten=Flatten()
        
        self.dense_2 = Dense(32, activation='relu')
        self.dropout_2 = Dropout(0.2)
        
        self.dense_3 = Dense(self.n_outputs)
        

    def call(self, x):
        x = self.dense_1(x)
        x = self.dropout_1(x)
        x = self.dense_2(x)
        x = self.dropout_2(x)
        x=self.flatten(x)
        x = self.dense_3(x)
        return x

    def getModel(self):
        inp = Input(shape=(self.n_steps,self.n_features,))
        x = MLP(self.n_steps,self.n_features, self.n_outputs)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model