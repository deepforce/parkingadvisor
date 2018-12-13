import os

import pandas as pd
from .parking_info import *
from .ev_geojson import *
from .streets_filter import *


def read_data(filename, col_names):
    '''
    Imports a .csv file with specific column as a pandas.DataFrame

    Attributes:
    ----------------
    filename: str
        The given filename
    col_names: list
        The given column names

    Returns
    ----------------
    dataframe_: pandas.DataFrame
        Dataframe with the specific columns
    '''
    if not os.path.exists(filename):
        raise NameError("No such file exists!")
    dataframe = pd.read_csv(filename)
    dataframe = dataframe[col_names]

    return dataframe
