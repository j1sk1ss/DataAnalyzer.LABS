import pandas as pd

from modules.data import Data


dataframe = Data(None)


def load_csv(file_path):
    global dataframe
    if file_path:
        df = pd.read_csv(file_path)
        dataframe = Data(df)


def data_is_loaded():
    if dataframe is None:
        return False

    return dataframe.data_body is not None


def get_graph(column):
    return list(dataframe.data_body[column])


def get_columns():
    return dataframe.data_body.columns.values


def summary():
    return dataframe.get_summary()


def predict(input_data: list):
    return dataframe.predict(input_data)


def get_data():
    return dataframe.data_body


def get_dataframe():
    return dataframe


def set_data(data):
    global dataframe
    dataframe = data


def set_target(target):
    global dataframe
    dataframe.target = target


def get_target():
    global dataframe
    return dataframe.target
