import pandas as pd

from modules.data import Data


dataframe = None


def load_csv(file_path):
    global dataframe
    if file_path:
        df = pd.read_csv(file_path)
        df = df.drop(columns=['Star color', 'Spectral Class'], axis=1)

        dataframe = Data(df)


def data_is_loaded():
    return dataframe is not None


def get_graph(column):
    return list(dataframe.data_body[column])


def get_columns():
    return dataframe.columns.values


def summary():
    return dataframe.get_summary()


def predict(input_data: list):
    return dataframe.predict(input_data)


def get_data():
    return dataframe.data_body


def set_data(data):
    global dataframe
    dataframe = data
