from Data import preprocess_data as pr
import numpy as np 
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import  Dense, Dropout, Input,Flatten

class FNN(tf.keras.Model):
    def __init__(self,n_steps,n_features,n_outputs=1):
        super(FNN, self).__init__()
        
        self.n_steps=n_steps
        self.n_features=n_features
        self.n_outputs=n_outputs
        
        self.dense_1 = Dense(256, activation='sigmoid')
        self.dropout_1 = Dropout(0.1)
        self.flatten = (Flatten())
        self.dense_2 = Dense(128, activation='softmax')
        
        self.dense_3 = Dense(n_outputs)
    
    def call(self, x):
        x = self.dense_1(x)
        x = self.flatten(x)
        x = self.dropout_1(x)

        x = self.dense_2(x)
        
        x = self.dense_3(x)

        return x
    def getModel(self):
        inp = Input(shape=(self.n_steps,self.n_features))
        x   = FNN(self.n_steps, self.n_features, self.n_outputs)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model