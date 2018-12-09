#!/usr/bin/env python
# coding: utf-8


"""This is a unittest for functions.py"""
import unittest

from functions import read_data
from functions import data_filter
from functions import select_street


class UnitTests(unittest.TestCase):
    """ This class is a unittest for functions.py"""
    def test_read_data(self):
        """ check the column name of the dataframe"""
        columns_known = ['Date Time','Unitdesc','Side', 'Parking_Spaces', 'Total_Vehicle_Count', 'Construction', 'Event Closure']
        dataframe = read_data('testfile1.csv', columns_known)
        self.assertEqual(dataframe.columns.tolist(), columns_known)
        wrong_column = ['Date Time','Unitdesc','Side', 'Total_Vehicle_Count', 'Event Closure']
        self.assertNotEqual(dataframe.columns.tolist(), wrong_column)
        
    def test_data_filter(self):
        """check there is no value of 'Yes' in specific column"""
        columns_known = ['Date Time','Unitdesc','Side', 'Parking_Spaces', 'Total_Vehicle_Count', 'Construction', 'Event Closure']
        dataframe = read_data('testfile1.csv', columns_known)
        values = ['Yes', 'yes', 'ERROR: #N/A']
        dataframe= data_filter(dataframe, 'Construction', values)
        dataframe = data_filter(dataframe, 'Event Closure', ['Yes'])
        self.assertEqual(set(dataframe['Construction']) , {'No'})
        self.assertEqual(set(dataframe['Event Closure']) , {'No'})
        
    def test_select_street(self):
        '''check the length of the selected data'''
        dataframe = read_data('testfile2.csv', ['Hour', 'Unitdesc', 'Parking_Spaces', 'Occupancy'])
        df = select_street(dataframe, '12TH AVE BETWEEN E CHERRY ST AND E COLUMBIA ST')
        self.assertEqual(len(df) , 3)
if __name__ == '__main__':
    unittest.main()

        

