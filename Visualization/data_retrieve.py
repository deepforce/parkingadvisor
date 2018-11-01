#!/usr/bin/env python
# coding=utf-8
from urllib import request
import pandas as pd
import os.path
def get_data(data_url, filename):
    '''
    data_url: this is the url of the data source
    filename: this is the file name you save
    '''
    if os.path.isfile(filename):
        print("The file %s already exists." %filename)
    else:
        print("Start to retrieve %s!" %filename)
        request.urlretrieve(data_url, filename)
        print("Finish!")
    
    df = pd.read_csv(filename)
    return df

