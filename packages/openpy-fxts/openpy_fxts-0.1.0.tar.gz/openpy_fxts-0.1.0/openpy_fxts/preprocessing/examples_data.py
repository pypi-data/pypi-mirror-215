import pandas as pd
import os
import pathlib


def _get_dataframe_raw():
    script_path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(
        pathlib.Path(script_path).joinpath('./BBDD_tests', 'HPC_raw_noNaN.csv'),
        header=0,
        parse_dates=['datetime'],
        index_col=['datetime'],
        #infer_datetime_format=False
    )


def _resample(
        data: pd.DataFrame = None,
        op: str = None,
        mean: bool = None,
):
    if data is None:
        print('Insert DataFrame')
        return None
    else:
        if bool:
            df_resample = data.resample(op).mean()
            print(df_resample.shape)
        else:
            df_resample = data.resample(op).sum()
            print(df_resample.shape)
        return df_resample


def hpc_dataframe(ts: str = '10min', mean: bool = True):
    data = _resample(
        _get_dataframe_raw(),
        op=ts,
        mean=mean
    )
    return data


def pump_sensor_dataframe():
    script_path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(
        pathlib.Path(script_path).joinpath('./BBDD_tests', 'sensor_final.csv'),
        index_col="timestamp",
        parse_dates=["timestamp"]
    )


