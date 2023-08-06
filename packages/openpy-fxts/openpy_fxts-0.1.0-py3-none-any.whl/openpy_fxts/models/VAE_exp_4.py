import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from tqdm import tqdm
from openpy_fxts.models.models_class import feat_lst, MyModel_exp4_normal, MyModel_exp4_tf

import tensorflow as tf
from tensorflow.python.client import device_lib

from .utils import _callbacks, _scaler_data, _historical_max_min, _examples_plots

def _lstm_train_data_transform(df, n_in, n_out, val_size, test_size):
    """
    Changes data to the format for LSTM training for sliding window approach
    """

    encoder_input, decoder_input, final_output = list(), list(), list()  # Prepare the list for the transformed data
    for i in range(df.shape[0]):  # Loop of the entire data set
        total_steps = i + n_in + n_out
        if total_steps >= df.shape[0]:  # if index is larger than the size of the dataset, we stop
            break
        end_enc_inp = i + n_in  # compute a new (sliding window) index for encoder input
        end_dec_inp = end_enc_inp + n_out - 1  # compute a new (sliding window) index for input steps
        final_out_end = end_enc_inp + n_out
        seq_enc_input = df[i:end_enc_inp]  # Get a sequence of data for x
        seq_dec_input = df[end_enc_inp:end_dec_inp]  # Get a sequence of data for x
        seq_final_out = df[end_enc_inp:final_out_end]
        encoder_input.append(seq_enc_input)  # Append the list with sequencies
        decoder_input.append(seq_dec_input)
        final_output.append(seq_final_out)
    encoder_input = np.array(encoder_input)  # Make final arrays
    decoder_input = np.array(decoder_input)
    final_output = np.array(final_output)
    train_size = round((encoder_input.shape[0] * (val_size + test_size)) / 100)
    train_size = encoder_input.shape[0] - train_size
    val_size = round((encoder_input.shape[0] * val_size) / 100)
    val_size = train_size + val_size
    encoder_input_train = encoder_input[:train_size]
    decoder_input_train = decoder_input[:train_size]
    final_output_train = final_output[:train_size]
    encoder_input_val = encoder_input[train_size:val_size]
    decoder_input_val = decoder_input[train_size:val_size]
    final_output_val = final_output[train_size:val_size]
    encoder_input_test = encoder_input[val_size:]
    decoder_input_test = decoder_input[val_size:]
    final_output_test = final_output[val_size:]

    train_dict, val_dict, test_dict = {}, {}, {}
    # Train
    train_dict['encoder_input_train'] = encoder_input_train
    train_dict['decoder_input_train'] = decoder_input_train
    train_dict['final_output_train'] = final_output_train
    # Validation
    val_dict['encoder_input_val'] = encoder_input_val
    val_dict['decoder_input_val'] = decoder_input_val
    val_dict['final_output_val'] = final_output_val
    # Test
    test_dict['encoder_input_test'] = encoder_input_test
    test_dict['decoder_input_test'] = decoder_input_test
    test_dict['final_output_test'] = final_output_test

    return train_dict, val_dict, test_dict


def lstm_train_data_transform_tf(df, n_in, n_out, val_size, test_size):
    """
    Changes data to the format for LSTM training for sliding window approach
    """

    encoder_input, decoder_input, final_output = list(), list(), list()  # Prepare the list for the transformed data
    for i in range(df.shape[0]):  # Loop of the entire data set
        total_steps = i + n_in + n_out
        if total_steps >= df.shape[0]:  # if index is larger than the size of the dataset, we stop
            break
        end_enc_inp = i + n_in  # compute a new (sliding window) index for encoder input
        end_dec_inp = end_enc_inp + n_out - 1  # compute a new (sliding window) index for input steps
        final_out_end = end_enc_inp + n_out
        seq_enc_input = df[i:end_enc_inp]  # Get a sequence of data for x
        seq_dec_input = df[end_enc_inp:end_dec_inp]  # Get a sequence of data for x
        seq_final_out = df[end_enc_inp:final_out_end]
        encoder_input.append(seq_enc_input)  # Append the list with sequencies
        decoder_input.append(seq_dec_input)
        final_output.append(seq_final_out)
    encoder_input = np.array(encoder_input)  # Make final arrays
    decoder_input = np.array(decoder_input)
    final_output = np.array(final_output)
    train_size = round((encoder_input.shape[0] * (val_size + test_size)) / 100)
    train_size = encoder_input.shape[0] - train_size
    val_size = round((encoder_input.shape[0] * val_size) / 100)
    val_size = train_size + val_size
    encoder_input_train = encoder_input[:train_size]
    decoder_input_train = decoder_input[:train_size]
    final_output_train = final_output[:train_size]
    encoder_input_val = encoder_input[train_size:val_size]
    decoder_input_val = decoder_input[train_size:val_size]
    final_output_val = final_output[train_size:val_size]
    encoder_input_test = encoder_input[val_size:]
    decoder_input_test = decoder_input[val_size:]
    final_output_test = final_output[val_size:]

    train_dict, val_dict, test_dict = {}, {}, {}
    # Train
    train_dict['encoder_input_train'] = encoder_input_train
    train_dict['decoder_input_train'] = decoder_input_train
    train_dict['final_output_train'] = final_output_train
    # Validation
    val_dict['encoder_input_val'] = encoder_input_val
    val_dict['decoder_input_val'] = decoder_input_val
    val_dict['final_output_val'] = final_output_val
    # Test
    test_dict['encoder_input_test'] = encoder_input_test
    test_dict['decoder_input_test'] = decoder_input_test
    test_dict['final_output_test'] = final_output_test

    return train_dict, val_dict, test_dict


class exp4_normal:

    def __init__(self, n_in=10, n_out=5, val_size=10, test_size=5, dataset=None):
        self.n_in = n_in
        self.n_out = n_out
        self.val_size = val_size
        self.test_size = test_size
        self.dataset = dataset

        self.batch_size = 64  # Batch size for training.
        self.epochs = 100  # Number of epochs to train for.
        self.units = 256  # no of lstm units
        self.features = dataset.shape[1]
        self.feat_lst = feat_lst  # adding 0 at the front to help in the very first iteration while creating layers in a loop


    def build_model(self, filepath):

        train_dict, val_dict, _ = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )
        train_dict, val_dict, _ = _scaler_data(train_dict, val_dict)
        model = MyModel_exp4_normal(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # without teacher forcing
        model.build(input_shape=(None, self.n_in, self.features))
        model.summary()
        # without teacher forcing
        model.fit(
            x=train_dict['encoder_input_train'],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                val_dict['encoder_input_val'],
                val_dict['final_output_val']
            ),
            callbacks=_callbacks(filepath, weights=True)
        )
        return model

    def _inference(self, input, model_new):
        train_dict_org, val_dict_org, test_dict_org = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )
        historical_max, historical_min = _historical_max_min(encoder_input_train=train_dict_org['encoder_input_train'])
        train_dict, val_dict, scaler = _scaler_data(train_dict_org, val_dict_org)
        input = scaler.transform(input)
        input = tf.expand_dims(input, 0)
        encoder_outputs, hidden, cell = model_new.layers[0](input)
        states = [hidden, cell]
        all_outputs = []
        final = model_new.layers[1](encoder_outputs, initial_state=states)
        final = model_new.layers[2](final)
        final = np.expand_dims(final, axis=1)
        all_outputs.append(final)
        for i in range(self.n_out - 1):
            input = input[:, 1:, :]
            input = tf.concat([input, all_outputs[-1]], axis=1)
            encoder_outputs, hidden, cell = model_new.layers[0](input)
            states = [hidden, cell]
            final = model_new.layers[1](encoder_outputs, initial_state=states)
            final = model_new.layers[2](final)
            final = np.expand_dims(final, axis=1)
            all_outputs.append(final)
        all_outputs = np.concatenate(all_outputs, axis=1)
        all_outputs = scaler.inverse_transform(all_outputs.reshape(-1, all_outputs.shape[-1])).reshape(all_outputs.shape)
        for i in range(all_outputs.shape[1]):
            for j in range(all_outputs.shape[2]):
                if all_outputs[:, i, j] < historical_min[0][0][j]:
                    all_outputs[:, i, j] = historical_min[0][0][j]
                elif all_outputs[:, i, j] > historical_max[0][0][j]:
                    all_outputs[:, i, j] = historical_max[0][0][j]
        return all_outputs

    def prediction(self, model_new):
        aux = exp4_tf(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]
        y_what = []
        for i in tqdm(range(test_dict['encoder_input_test'].shape[0])):
            x = test_dict['encoder_input_test'][i].copy()
            x = aux._inference(
                input=x,
                model_new=model_new
            )
            y_what.append(x)
        y_what = np.concatenate(y_what, 0)
        return y_what

    def metrics(self, pred):
        test_dict = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )[2]
        return mean_squared_error(
            test_dict['final_output_test'].reshape(-1, test_dict['final_output_test'].shape[-1]),
            pred.reshape(-1, pred.shape[-1]),
            squared=False
        )

    def plot_results(self, pred):
        final_output_test = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )[2]['final_output_test']
        features = final_output_test.shape[2]

        fig, axs = plt.subplots(int(features), 1, layout=None)
        aux = 0
        for ax, i in zip(axs.flat, range(features)):
            _examples_plots(ax, final_output_test, pred, i)
            aux += 1

        plt.show()


class exp4_tf:

    def __init__(self, n_in=10, n_out=5, val_size=10, test_size=5, dataset=None):
        self.n_in = n_in
        self.n_out = n_out
        self.val_size = val_size
        self.test_size = test_size
        self.dataset = dataset

        self.batch_size = 64  # Batch size for training.
        self.epochs = 100  # Number of epochs to train for.
        self.units = 256  # no of lstm units
        self.features = dataset.shape[1]
        self.feat_lst = feat_lst  # adding 0 at the front to help in the very first iteration while creating layers in a loop


    def build_model(self, filepath):

        train_dict, val_dict, _ = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )
        train_dict, val_dict, _ = _scaler_data(train_dict, val_dict)
        model = MyModel_exp4_tf(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[
            (None, self.n_in, self.features),
            (None, self.n_out - 1, self.features)
        ])
        model.summary()
        # teacher forcing
        model.fit(
            x=[train_dict['encoder_input_train'], train_dict['decoder_input_train']],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                [val_dict['encoder_input_val'], val_dict['decoder_input_val']],
                val_dict['final_output_val']
            ),
            callbacks=_callbacks(filepath, weights=True)
        )
        return model

    def _inference(self, input, model_new):
        train_dict_org, val_dict_org, test_dict_org = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )
        historical_max, historical_min = _historical_max_min(encoder_input_train=train_dict_org['encoder_input_train'])
        train_dict, val_dict, scaler = _scaler_data(train_dict_org, val_dict_org)
        input = scaler.transform(input)
        input = tf.expand_dims(input, 0)
        encoder_outputs, hidden, cell = model_new.layers[0](input)
        states = [hidden, cell]
        all_outputs = []
        final = model_new.layers[1](encoder_outputs, initial_state=states)
        final = model_new.layers[2](final)
        final = np.expand_dims(final, axis=1)
        all_outputs.append(final)
        for i in range(self.n_out - 1):
            input = input[:, 1:, :]
            input = tf.concat([input, all_outputs[-1]], axis=1)
            encoder_outputs, hidden, cell = model_new.layers[0](input)
            states = [hidden, cell]
            final = model_new.layers[1](encoder_outputs, initial_state=states)
            final = model_new.layers[2](final)
            final = np.expand_dims(final, axis=1)
            all_outputs.append(final)
        all_outputs = np.concatenate(all_outputs, axis=1)
        all_outputs = scaler.inverse_transform(
            all_outputs.reshape(-1, all_outputs.shape[-1])
        ).reshape(all_outputs.shape)
        for i in range(all_outputs.shape[1]):
            for j in range(all_outputs.shape[2]):
                if all_outputs[:, i, j] < historical_min[0][0][j]:
                    all_outputs[:, i, j] = historical_min[0][0][j]
                elif all_outputs[:, i, j] > historical_max[0][0][j]:
                    all_outputs[:, i, j] = historical_max[0][0][j]
        return all_outputs

    def prediction(self, model_new):
        aux = exp4_tf(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]
        y_what = []
        for i in tqdm(range(test_dict['encoder_input_test'].shape[0])):
            x = test_dict['encoder_input_test'][i].copy()
            x = aux._inference(
                input=x,
                model_new=model_new
            )
            y_what.append(x)
        y_what = np.concatenate(y_what, 0)
        return y_what

    def metrics(self, pred):
        test_dict = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )[2]
        return mean_squared_error(
            test_dict['final_output_test'].reshape(-1, test_dict['final_output_test'].shape[-1]),
            pred.reshape(-1, pred.shape[-1]),
            squared=False
        )

    def plot_results(self, pred):
        final_output_test = _lstm_train_data_transform(
            self.dataset,
            self.n_in,
            self.n_out,
            self.val_size,
            self.test_size
        )[2]['final_output_test']
        features = final_output_test.shape[2]

        fig, axs = plt.subplots(int(features), 1, layout=None)
        aux = 0
        for ax, i in zip(axs.flat, range(features)):
            _examples_plots(ax, final_output_test, pred, i)
            aux += 1

        plt.show()