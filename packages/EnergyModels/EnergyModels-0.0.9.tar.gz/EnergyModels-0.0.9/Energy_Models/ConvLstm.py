import numpy as np 
import pandas as pd
import tensorflow as tf
from   tensorflow.keras.layers import  Dense, Dropout, LSTM, Input,Flatten,ConvLSTM2D,BatchNormalization

class ConvLstm(tf.keras.Model):
    def __init__(self, n_steps, n_features, n_outputs=1):
        super(ConvLstm, self).__init__()
        self.n_steps = n_steps
        self.n_features = n_features
        self.n_outputs = n_outputs
        self.convlstm_1 = ConvLSTM2D(
                         filters = 64, kernel_size = (10, 1),                       
                         padding = 'same',input_shape = (1,1,self.n_steps,self.n_features), 
                         return_sequences = True)
        self.convlstm_2 = ConvLSTM2D(
                         filters = 64, kernel_size = (5, 1), 
                         padding='same',
                         return_sequences = True)
        self.convlstm_3 = ConvLSTM2D(
                         filters = 64, kernel_size = (10, 1), 
                         padding='same',
                         return_sequences = True)
        self.convlstm_4 = ConvLSTM2D(
                         filters = 64, kernel_size = (5, 1), 
                         padding='same',
                         return_sequences = True)
        self.dropout_1 = Dropout(0.3)
        self.dropout_2 = Dropout(0.2)
        self.dropout_3 = Dropout(0.2)
        self.Batch_2=BatchNormalization()
        self.Batch_3=BatchNormalization()
        self.Batch_4=BatchNormalization()
        self.flatten=Flatten()

        self.dense_1 = Dense(units=64,activation = 'relu')
        self.dense_2 = Dense(self.n_outputs)

    def call(self, x):
        x = self.convlstm_1(x)
        x = self.dropout_1(x)
        x = self.convlstm_2(x)
        x = self.dropout_2(x)
        x = self.convlstm_3(x)
        x = self.dropout_3(x)
        x = self.convlstm_4(x)
        x=self.flatten(x)
        x = self.dense_1(x)
        x = self.dense_2(x)

        return x

    def getModel(self):
        inp = Input(shape=(1,1,self.n_steps,self.n_features))
        x = ConvLstm(self.n_steps, self.n_features, self.n_outputs)(inp)
        model = tf.keras.Model(inputs=inp, outputs=x)
        return model