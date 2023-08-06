import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from tqdm import tqdm
from .utils import _callbacks

import tensorflow as tf
from tensorflow.python.client import device_lib
from openpy_fxts.models.models_class import feat_lst


def _lstm_train_data_transform_case_A(df, n_in, n_out, val_size, test_size):
    """
    Changes data to the format for LSTM training  for sliding window approach
    """
    encoder_input, final_output = list(), list()  # Prepare the list for the transformed data
    train_val = round(df.shape[0] * ((100 - test_size) / 100))
    for i in range(train_val):  # Loop of the entire data set
        total_steps = i + n_in + 1
        if total_steps >= train_val:  # if index is larger than the size of the dataset, we stop
            break
        end_enc_inp = i + n_in  # compute a new (sliding window) index for encoder input
        final_out_end = end_enc_inp + 1
        seq_enc_input = df[i:end_enc_inp]  # Get a sequence of data for x
        seq_final_out = df[end_enc_inp:final_out_end]
        encoder_input.append(seq_enc_input)  # Append the list with sequencies
        final_output.append(seq_final_out)
    encoder_input = np.array(encoder_input)  # Make final arrays
    final_output = np.array(final_output)
    train_size = round(df.shape[0] * ((100 - (val_size + test_size)) / 100))
    encoder_input_train = encoder_input[:train_size]
    final_output_train = final_output[:train_size]
    encoder_input_val = encoder_input[train_size:]
    final_output_val = final_output[train_size:]
    encoder_input, final_output = list(), list()
    for i in range(df[train_val:].shape[0]):  # Loop of the entire data set
        total_steps = i + n_in + n_out
        if total_steps >= df[train_val:].shape[0]:  # if index is larger than the size of the dataset, we stop
            break
        end_enc_inp = i + n_in  # compute a new (sliding window) index for encoder input
        final_out_end = end_enc_inp + n_out
        seq_enc_input = df[i:end_enc_inp]  # Get a sequence of data for x
        seq_final_out = df[end_enc_inp:final_out_end]
        encoder_input.append(seq_enc_input)  # Append the list with sequencies
        final_output.append(seq_final_out)
    encoder_input = np.array(encoder_input)  # Make final arrays
    final_output = np.array(final_output)
    encoder_input_test = encoder_input
    final_output_test = final_output

    train_dict, val_dict, test_dict = {}, {}, {}
    # Train
    train_dict['encoder_input_train'] = encoder_input_train
    train_dict['final_output_train'] = final_output_train
    # Validation
    val_dict['encoder_input_val'] = encoder_input_val
    val_dict['final_output_val'] = final_output_val
    # Test
    test_dict['encoder_input_test'] = encoder_input_test
    test_dict['final_output_test'] = final_output_test

    return train_dict, val_dict, test_dict


def _lstm_train_data_transform_case_B(df, n_in, n_out, val_size, test_size):
    """
    Changes data to the format for LSTM training for sliding window approach
    """
    encoder_input, final_output = list(), list()  # Prepare the list for the transformed data
    for i in range(df.shape[0]):  # Loop of the entire data set
        total_steps = i + n_in + n_out
        if total_steps >= df.shape[0]:  # if index is larger than the size of the dataset, we stop
            break
        end_enc_inp = i + n_in  # compute a new (sliding window) index for encoder input
        final_out_end = end_enc_inp + n_out
        seq_enc_input = df[i:end_enc_inp]  # Get a sequence of data for x
        seq_final_out = df[end_enc_inp:final_out_end]
        encoder_input.append(seq_enc_input)  # Append the list with sequencies
        final_output.append(seq_final_out)
    encoder_input = np.array(encoder_input)  # Make final arrays
    final_output = np.array(final_output)
    train_size = round((encoder_input.shape[0] * (val_size + test_size)) / 100)
    train_size = encoder_input.shape[0] - train_size
    val_size = round((encoder_input.shape[0] * val_size) / 100)
    val_size = train_size + val_size

    encoder_input_train = encoder_input[:train_size]
    final_output_train = final_output[:train_size]
    encoder_input_val = encoder_input[train_size:val_size]
    final_output_val = final_output[train_size:val_size]
    encoder_input_test = encoder_input[val_size:]
    final_output_test = final_output[val_size:]

    train_dict, val_dict, test_dict = {}, {}, {}
    # Train
    train_dict['encoder_input_train'] = encoder_input_train
    train_dict['final_output_train'] = final_output_train
    # Validation
    val_dict['encoder_input_val'] = encoder_input_val
    val_dict['final_output_val'] = final_output_val
    # Test
    test_dict['encoder_input_test'] = encoder_input_test
    test_dict['final_output_test'] = final_output_test

    return train_dict, val_dict, test_dict


def historical_max_min(encoder_input_train):
    historical_max = np.expand_dims(
        np.max(encoder_input_train.reshape(-1, encoder_input_train.shape[-1]), axis=0, keepdims=True), 0)
    historical_min = np.expand_dims(
        np.min(encoder_input_train.reshape(-1, encoder_input_train.shape[-1]), axis=0, keepdims=True), 0)
    return historical_max, historical_min


def scaler_data(train_dict, val_dict):
    scaler = StandardScaler()

    encoder_input_train = scaler.fit_transform(
        train_dict['encoder_input_train'].reshape(
            -1, train_dict['encoder_input_train'].shape[-1]
        )
    ).reshape(train_dict['encoder_input_train'].shape)

    final_output_train = scaler.transform(
        train_dict['final_output_train'].reshape(-1, train_dict['final_output_train'].shape[-1])
    ).reshape(train_dict['final_output_train'].shape)

    encoder_input_val = scaler.transform(
        val_dict['encoder_input_val'].reshape(-1, val_dict['encoder_input_val'].shape[-1])
    ).reshape(val_dict['encoder_input_val'].shape)

    final_output_val = scaler.transform(
        val_dict['final_output_val'].reshape(-1, val_dict['final_output_val'].shape[-1])
    ).reshape(val_dict['final_output_val'].shape)

    train_dict_scaler, val_dict_scaler = {}, {}
    # Train
    train_dict_scaler['encoder_input_train'] = encoder_input_train
    train_dict_scaler['final_output_train'] = final_output_train
    # Validation
    val_dict_scaler['encoder_input_val'] = encoder_input_val
    val_dict_scaler['final_output_val'] = final_output_val

    return train_dict_scaler, val_dict_scaler, scaler


class exp3_case_A:

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

        train_dict, val_dict, _ = _lstm_train_data_transform_case_A(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)
        train_dict, val_dict, _ = scaler_data(train_dict, val_dict)
        # Define an input sequence and process it.
        input = tf.keras.layers.Input(shape=(self.n_in, self.features))
        lstm1 = tf.keras.layers.LSTM(self.units, return_sequences=True, return_state=True, dtype='float64')
        lstm1_output, hidden, cell = lstm1(input)
        states = [hidden, cell]
        lstm2 = tf.keras.layers.LSTM(self.units, dtype='float64')
        lstm2_output = lstm2(lstm1_output, initial_state=states)
        lstm2_dense = tf.keras.layers.Dense(self.features, dtype='float64')
        lstm2_output = tf.expand_dims(lstm2_dense(lstm2_output), 1)
        model = tf.keras.models.Model(input, lstm2_output)
        model.compile(optimizer='adam', loss='mse')
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
            callbacks=_callbacks(filepath, model=True)
        )

        return model

    def _inference(self, input, model_new):
        train_dict_org, val_dict_org, test_dict_org = _lstm_train_data_transform_case_A(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )
        historical_max, historical_min = historical_max_min(encoder_input_train=train_dict_org['encoder_input_train'])
        train_dict, val_dict, scaler = scaler_data(train_dict_org, val_dict_org)
        input = scaler.transform(input)
        input = tf.expand_dims(input, 0)
        all_outputs = []
        pred = model_new.predict(input, verbose=0)
        all_outputs.append(pred)
        for i in range(self.n_out - 1):
            input = input[:, 1:, :]
            input = tf.concat([input, all_outputs[-1]], axis=1)
            pred = model_new.predict(input, verbose=0)
            all_outputs.append(pred)
        all_outputs = np.concatenate(all_outputs, axis=1)
        all_outputs = scaler.inverse_transform(all_outputs.reshape(-1, all_outputs.shape[-1])).reshape(
            all_outputs.shape)
        for i in range(all_outputs.shape[1]):
            for j in range(all_outputs.shape[2]):
                if all_outputs[:, i, j] < historical_min[0][0][j]:
                    all_outputs[:, i, j] = historical_min[0][0][j]
                elif all_outputs[:, i, j] > historical_max[0][0][j]:
                    all_outputs[:, i, j] = historical_max[0][0][j]
        return all_outputs

    def prediction(self, model_new):
        aux = exp3_case_A(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform_case_A(
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
        test_dict = _lstm_train_data_transform_case_A(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]
        return mean_squared_error(
            test_dict['final_output_test'].reshape(-1, test_dict['final_output_test'].shape[-1]),
            pred.reshape(-1, pred.shape[-1]),
            squared=False
        )

    def plot_results(self, pred):
        final_output_test = _lstm_train_data_transform_case_A(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]['final_output_test']
        features = final_output_test.shape[2]

        fig, axs = plt.subplots(int(features), 1, layout=None)
        aux = 0
        for ax, i in zip(axs.flat, range(features)):
            example_plot(ax, final_output_test, pred, i)
            aux += 1

        plt.show()


class exp3_case_B:

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

        train_dict, val_dict, _ = _lstm_train_data_transform_case_B(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)
        train_dict, val_dict, _ = scaler_data(train_dict, val_dict)
        # Define an input sequence and process it.
        input = tf.keras.layers.Input(shape=(self.n_in, self.features))
        lstm1 = tf.keras.layers.LSTM(self.units, return_sequences=True, return_state=True, dtype='float64')
        lstm1_output, hidden, cell = lstm1(input)
        states = [hidden, cell]
        lstm2 = tf.keras.layers.LSTM(self.units, return_sequences=True, dtype='float64')
        lstm2_output = lstm2(lstm1_output, initial_state=states)
        lstm2_dense = tf.keras.layers.Dense(self.features, dtype='float64')
        lstm2_output = lstm2_dense(lstm2_output)
        model = tf.keras.models.Model(input, lstm2_output)
        model.compile(optimizer='adam', loss='mse')
        model.summary()
        # without teacher forcing

        model.fit(
            x=train_dict['encoder_input_train'],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                val_dict['encoder_input_val'],
                val_dict['final_output_val']),
            callbacks=_callbacks(filepath, model=True)
        )


        return model

    def _inference(self, input, model_new):
        train_dict_org, val_dict_org, test_dict_org = _lstm_train_data_transform_case_B(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )
        historical_max, historical_min = historical_max_min(encoder_input_train=train_dict_org['encoder_input_train'])
        train_dict, val_dict, scaler = scaler_data(train_dict_org, val_dict_org)

        input = scaler.transform(input)
        input = tf.expand_dims(input, 0)
        prediction = model_new.predict(input, verbose=0)
        prediction = scaler.inverse_transform(prediction.reshape(-1, prediction.shape[-1])).reshape(prediction.shape)
        for i in range(prediction.shape[1]):
            for j in range(prediction.shape[2]):
                if prediction[:, i, j] < historical_min[0][0][j]:
                    prediction[:, i, j] = historical_min[0][0][j]
                elif prediction[:, i, j] > historical_max[0][0][j]:
                    prediction[:, i, j] = historical_max[0][0][j]
        return prediction

    def prediction(self, model_new):
        aux = exp3_case_B(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform_case_B(
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
        test_dict = _lstm_train_data_transform_case_B(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]
        return mean_squared_error(
            test_dict['final_output_test'].reshape(-1, test_dict['final_output_test'].shape[-1]),
            pred.reshape(-1, pred.shape[-1]),
            squared=False
        )

    def plot_results(self, pred):
        final_output_test = _lstm_train_data_transform_case_B(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size
        )[2]['final_output_test']
        features = final_output_test.shape[2]

        fig, axs = plt.subplots(int(features), 1, layout=None)
        aux = 0
        for ax, i in zip(axs.flat, range(features)):
            example_plot(ax, final_output_test, pred, i)
            aux += 1

        plt.show()

def example_plot(ax, final_output_test, pred, i, fontsize=12, hide_labels=False):
    ax.plot(final_output_test.reshape(-1, final_output_test.shape[-1])[:, i], c='blue', label="measured")
    ax.plot(pred.reshape(-1, pred.shape[-1])[:, i], c='red', label="prediction")

    ax.locator_params(nbins=3)
    if hide_labels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    else:
        ax.set_xlabel(f'Feature {i + 1} across all timesteps', fontsize=fontsize)
        ax.set_ylabel(f'F_{i + 1}', fontsize=fontsize)
        # ax.set_title('Title', fontsize=fontsize)
    mse = mean_squared_error(


        final_output_test.reshape(-1, final_output_test.shape[-1])[:, i],
        pred.reshape(-1, pred.shape[-1])[:, i],
        squared=False
    )
    print(f'Feature {i + 1} MSE: {mse}')
