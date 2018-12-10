#!/usr/bin/env python
# coding: utf-8
"""
This module cleans 2 datasets ('Annual_parking_study.csv', 'Blockface
.csv'), summaries The parking utility per hour of the day from annual
parking study, and generates subset datasets for future use.
"""

import pandas as pd

def data_filter(dataframe, col, values):
    '''
    Drop the rows containing specific values in specific columns

    Attributes:
    ---------------
    dataframe: DataFrame
        The given DataFrame to clean
    col: str
        The column names of the insepected columns
    values: List
        The specific values that need to drop

    Returns
    --------------
    dataframe: DataFrame
        a clean Dataframe without unwanted values in specific columns
    '''

    for val in values:
        dataframe = dataframe[dataframe[col] != val]

    return dataframe


def modify_end_time(dataframe, end_col):
    '''
    Changes the hour of datetime (e.g. 8:59) into the end hour number
    (i.e. 9)

    Attributes:
    ---------------
    dataframe: DataFrame
        The DataFrame to edit
    end_col: list
        The datetime columns to change
    '''

    for col in  end_col:
        dataframe.loc[:, col] = dataframe.loc[:, col] + 1


def convert_datetime_to_h(dataframe, cols):
    '''
    Extracts the hour of the day (i.e. 8) from minute format (e.g. 480) as index

    Attributes:
    ----------------
    dataframe: DataFrame
        The DataFrame to edit
    cols: list
        The columns containg datetime
    '''
    for name in cols:
        dataframe.loc[:, name] = pd.TimedeltaIndex(dataframe.loc[:, name], unit='m')
        dataframe.loc[:, name] = pd.DatetimeIndex(dataframe.loc[:, name]).hour
