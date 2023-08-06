import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import lag_plot
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from tqdm import tqdm

import tensorflow as tf
from tensorflow.python.client import device_lib

from .utils import _callbacks, _scaler_data, _historical_max_min, _examples_plots
from openpy_fxts.models.models_class import feat_lst
from openpy_fxts.models.models_class import MyModel_exp2_hybrid_normal
from openpy_fxts.models.models_class import MyModel_exp2_hybrid_tf
from openpy_fxts.models.models_class import MyModel_exp2_separate_normal
from openpy_fxts.models.models_class import MyModel_exp2_separate_tf
from openpy_fxts.models.models_class import MyModel_exp2_shared_normal
from openpy_fxts.models.models_class import MyModel_exp2_shared_normal_luongs_concat_attention
from openpy_fxts.models.models_class import MyModel_exp2_shared_normal_luongs_dot_attention
from openpy_fxts.models.models_class import MyModel_exp2_shared_normal_luongs_general_attention
from openpy_fxts.models.models_class import MyModel_exp2_shared_tf
from openpy_fxts.models.models_class import MyModel_exp2_shared_tf_luongs_general_attention
from openpy_fxts.models.models_class import MyModel_exp2_shared_tf_luongs_concat_attention
from openpy_fxts.models.models_class import MyModel_exp2_shared_tf_luongs_dot_attention


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


class exp2_hybrid_normal:

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
        model = MyModel_exp2_hybrid_normal(
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
        encoder_input = input
        all_outputs = []
        layers = [model_new.layers[i: i + 3] for i in range(0, len(model_new.layers), 3)]
        for i in range(len(feat_lst) - 1):
            outputs = []
            enc_input = encoder_input[:, :, feat_lst[i]:feat_lst[i + 1]]
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = layers[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
            final = layers[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.n_out - 1):
                cur_vec = final
                final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
                final = layers[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = np.concatenate(all_outputs, axis=2)
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
        aux = exp2_hybrid_normal(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
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


class exp2_hybrid_tf:

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
        model = MyModel_exp2_hybrid_tf(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
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
        encoder_input = input
        all_outputs = []
        layers = [model_new.layers[i: i + 3] for i in range(0, len(model_new.layers), 3)]
        for i in range(len(feat_lst) - 1):
            outputs = []
            enc_input = encoder_input[:, :, feat_lst[i]:feat_lst[i + 1]]
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = layers[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
            final = layers[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.n_out - 1):
                cur_vec = final
                final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
                final = layers[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = np.concatenate(all_outputs, axis=2)
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
        aux = exp2_hybrid_tf(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_separate_normal:

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
        model = MyModel_exp2_separate_normal(
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
        encoder_input = input
        all_outputs = []
        layers = [model_new.layers[i: i + 3] for i in range(0, len(model_new.layers), 3)]
        for i in range(self.features):
            outputs = []
            enc_input = tf.expand_dims(encoder_input[:, :, i], 2)
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = layers[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
            final = layers[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.n_out - 1):
                cur_vec = final
                final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
                final = layers[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = np.concatenate(all_outputs, axis=2)
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
        aux = exp2_separate_normal(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_separate_tf:

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
        model = MyModel_exp2_separate_tf(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
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
        encoder_input = input
        all_outputs = []
        layers = [model_new.layers[i: i + 3] for i in range(0, len(model_new.layers), 3)]
        for i in range(self.features):
            outputs = []
            enc_input = tf.expand_dims(encoder_input[:, :, i], 2)
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = layers[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
            final = layers[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.n_out - 1):
                cur_vec = final
                final, hidden, cell = layers[i][1](cur_vec, initial_state=states)
                final = layers[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = np.concatenate(all_outputs, axis=2)
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
        aux = exp2_separate_tf(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_normal:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_normal(
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        _, hidden, cell = model_new.layers[0](encoder_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        final, hidden, cell = model_new.layers[1](cur_vec, initial_state=states)
        final = model_new.layers[2](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            cur_vec = final
            final, hidden, cell = model_new.layers[1](cur_vec, initial_state=states)
            final = model_new.layers[2](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_normal(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_normal_luongs_concat_attention:

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
        model = MyModel_exp2_shared_normal_luongs_concat_attention(
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_normal_luongs_concat_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_normal_luongs_dot_attention:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_normal_luongs_dot_attention(
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_normal_luongs_dot_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_normal_luongs_general_attention:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_normal_luongs_general_attention(
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_normal_luongs_general_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_tf:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_tf(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
        model.summary()
        # teacher forcing
        model.fit(
            x=[train_dict['encoder_input_train'], train_dict['decoder_input_train']],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                [val_dict['encoder_input_val'], val_dict['decoder_input_val']],
                val_dict['final_output_val']),
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        _, hidden, cell = model_new.layers[0](encoder_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        final, hidden, cell = model_new.layers[1](cur_vec, initial_state=states)
        final = model_new.layers[2](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            cur_vec = final
            final, hidden, cell = model_new.layers[1](cur_vec, initial_state=states)
            final = model_new.layers[2](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_tf(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_tf_luongs_general_attention:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_tf_luongs_general_attention(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
        model.summary()
        # teacher forcing
        model.fit(
            x=[train_dict['encoder_input_train'], train_dict['decoder_input_train']],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                [val_dict['encoder_input_val'], val_dict['decoder_input_val']],
                val_dict['final_output_val']),
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_tf_luongs_general_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_tf_luongs_concat_attention:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_tf_luongs_concat_attention(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
        model.summary()
        # teacher forcing
        model.fit(
            x=[train_dict['encoder_input_train'], train_dict['decoder_input_train']],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                [val_dict['encoder_input_val'], val_dict['decoder_input_val']],
                val_dict['final_output_val']),
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_tf_luongs_concat_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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


class exp2_shared_tf_luongs_dot_attention:

    def __init__(self, n_in=11, n_out=5, val_size=10, test_size=5, dataset=None):
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
        model = MyModel_exp2_shared_tf_luongs_dot_attention(
            self.n_in,
            self.n_out,
            self.features,
            self.units
        )
        model.compile(optimizer='adam', loss='mse')
        # teacher forcing
        model.build(input_shape=[(None, self.n_in, self.features), (None, self.n_out - 1, self.features)])
        model.summary()
        # teacher forcing
        model.fit(
            x=[train_dict['encoder_input_train'], train_dict['decoder_input_train']],
            y=train_dict['final_output_train'],
            batch_size=self.batch_size,
            epochs=self.epochs,
            validation_data=(
                [val_dict['encoder_input_val'], val_dict['decoder_input_val']],
                val_dict['final_output_val']),
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
        encoder_input = input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = model_new.layers[0](encoder_input)
        context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
        final = model_new.layers[3](final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.n_out - 1):
            context_vector, attention_weights = model_new.layers[1](hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = model_new.layers[2](cur_vec, initial_state=states)
            final = model_new.layers[3](final)
            all_outputs.append(final)
            states = [hidden, cell]
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

        aux = exp2_shared_tf_luongs_dot_attention(self.n_in, self.n_out, self.val_size, self.test_size, self.dataset)
        test_dict = _lstm_train_data_transform(
            df=self.dataset,
            n_in=self.n_in,
            n_out=self.n_out,
            val_size=self.val_size,
            test_size=self.test_size)[2]
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
