#!/usr/bin/env python
# coding: utf-8

'''This is a unittest for parking_info.py'''
import unittest
import pandas as pd
import numpy as np

import sys
sys.path.append("..")
import data.clean_up as cln


class UnitTests(unittest.TestCase):
    ''' This class is a unittest for parking_info.py'''
    
    def test_data_filter(self):
        '''check there is no specific value in specific column'''
        df = pd.DataFrame({'a' : [1, 2, 3, 4, 5], 'b' : [10, 20, 30, 40 ,50], 'c' : [100, 200, 300, 400, 500]})
        df= cln.data_filter(df, 'a', [2, 3])
        df = cln.data_filter(df, 'b', [10, 40])
        self.assertEqual(len(df) , 1)
        self.assertEqual(df.loc[4]['c'] , 500)
        
    def test_modify_end_time(self):
        '''check the value of dataframe after running the function above'''
        df = pd.DataFrame({'a' : [1, 2, 3, 4, 5], 'b' : [10, 20, 30, 40 ,50], 'c' : [100, 200, 300, 400, 500]})
        cln.modify_end_time(df, 'b')
        self.assertEqual(df.loc[0]['b'], 11)
        self.assertEqual(df.loc[2]['b'], 31)
        self.assertEqual(df.loc[4]['b'], 51)
        self.assertNotEqual(df.loc[3]['b'], 40)
        
    def test_convert_datetime_to_h(self):
        '''check specific data after running function above'''
        df = pd.DataFrame({'a' : [1, 2, 3, 4, 5], 'b' : [10, 20, 30, 40 ,50], 'c' : [479, 539, 599, 659, 719]})
        cln.modify_end_time(df, 'c')
        cln.convert_datetime_to_h(df, 'c')
        self.assertEqual(df.loc[0]['c'], 8)
        self.assertEqual(df.loc[2]['c'], 10)
        self.assertEqual(df.loc[4]['c'], 12)
        self.assertNotEqual(df.loc[3]['c'], 10)
        
    def test_all_type(self):
        '''check the value of corresponding key'''
        df = pd.DataFrame({'EV Connector Types' : ['Type1 Type2 Type3 Type4', 'Type1 Type3 Type2', 
                                          'Type2 Type1 Type3', 'Type1', 'Type4 Type1', 'Type3 Type1',
                                           'Type3 Type1']})
        dic = cln.all_type(df)
        self.assertEqual(dic['Type1'], 7)
        self.assertEqual(dic['Type2'], 3)
        self.assertEqual(dic['Type3'], 5)
        self.assertNotEqual(dic['Type4'], 3)
        
    def test_ev_level_tf(self):
        '''check the value of specific column'''
        df = pd.DataFrame({'num' : [np.inf, 0, 1, np.NINF, np.nan]})
        df = cln.ev_level_tf(df, 'num', 'res')
        self.assertEqual(df.loc[1]['res'], True)
        self.assertEqual(df.loc[3]['res'], False)
        self.assertEqual(df.loc[4]['res'], False)
        self.assertNotEqual(df.loc[2]['res'], False)
        
    def test_ev_connector_tf(self):
        '''check the value of specific column'''
        df = pd.DataFrame({'EV Connector Types' : ['Type1 Type2 Type3 Type4', 'Type1 Type3 Type2', 
                                          'Type2 Type1 Type3', 'Type1', 'Type4 Type1', 'Type3 Type1',
                                           'Type3 Type1']})
        df = cln.ev_connector_tf(df, ['Type1', 'Type2', 'Type3', 'Type4'])
        self.assertEqual(df.loc[1]['Type1'], True)
        self.assertEqual(df.loc[3]['Type2'], False)
        self.assertEqual(df.loc[5]['Type3'], True)
        self.assertEqual(df.loc[3]['Type4'], False)
        
if __name__ == '__main__':
    unittest.main()

