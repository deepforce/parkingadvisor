#!/usr/bin/env python
# coding: utf-8

# In[10]:


import os.path
import pandas as pd
import numpy as np
from datetime import datetime


# In[11]:


#read data
def read_data(filename, col_names):
    '''
    Inputt: filename: String
            col_names: List
            given filename (csv) and column names that we want to import
    Output: return an original dataframe with the specific columns
    '''
    if not os.path.exists(filename):
        raise NameError("No such file exists!")
    df = pd.read_csv(filename)
    df = df[col_names]
    return df


# In[12]:


#keep the specific col excluding specific value
def data_filter(df, col, values):
    '''
    Input: df: dataframe
           col: String
           values: List
           given a dataframe, for specific column, we exclude specific values that we dont want include
    Output: return a new dataframe, without specific values of one column
    '''
    for val in values:
        df = df[df[col] != val]
    return df


# In[13]:


#select specific street name
def select_street(df, street_name):
    '''
    Input: df: dataframe
           street_name: String
           given a dataframe, group rows with same street name and hour by averaging other columns
    Output: return a dataframe with all the rows with spefic street name and different hour
    '''
    df = df[df['Unitdesc'] == street_name]
    df = df.groupby(['Hour', 'Unitdesc'] ,as_index = False)['Parking_Spaces', 'Occupancy'].mean()
    return df


# In[14]:


#modify the end time of all rates
def modify_end_time(df, end_col):
    '''
    Input: df: dataframe
           end_col: List
           given a dataframe, for all the columns we specify, add the values by one
    Output: Null
    '''
    for col in  end_col:
        df.loc[:, col] = df.loc[:, col] + 1


# In[15]:


#convert minutes to datetime
def convertDayTime(df, cols):
    '''
    Input: df: dataframe
           cols: List
           given a dataframe, convert specific columns from minute to datetime, and replace original value with hour
    Output: Null
    '''
    for name in cols:
        df.loc[:, name] =  pd.TimedeltaIndex(df.loc[:, name], unit='m')
        df.loc[:, name] =  pd.DatetimeIndex(df.loc[:, name]).hour


# In[ ]:




