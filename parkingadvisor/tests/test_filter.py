"""
Testing the filtering data module
"""

from datetime import datetime
import numpy as np
import pandas as pd

from parkingadvisor import filter


TEST_STREET_NAME = '10TH AVE BETWEEN E MADISON ST AND E SENECA ST'

def test_model_flow():
    """
    Testing the interpolation of parking occupancy data to generate
    a smoothed dataframe over 12 am-12 pm
    """
    # Use the first 20 rows to create a small dataframe
    # including street name '10TH AVE BETWEEN E MADISON ST AND E SENECA ST'
    df_test = pd.read_csv(filter._FLOW_RAW)
    street = df_test.loc[df_test['UNITDESC'] == TEST_STREET_NAME]
    df_result = filter._model_flow(street)

    assert np.array_equal(df_result.columns.values, ['TIME', 'OCCUPANCY'])
    assert df_result['TIME'].min() == 0 and df_result['TIME'].max() == 24
    assert df_result['OCCUPANCY'].any() >= 0


def test_loc_period():
    """
    Testing the fuction which create the rate of all streets at specific time
    """
    # Check the results in 5 different time
    test_data = pd.DataFrame(data={'UNITDESC': TEST_STREET_NAME,
                                   'WKD_START1': 8,
                                   'WKD_START2': 11,
                                   'WKD_START3':17,
                                   'WKD_END': 22,
                                   'WKD_RATE1': 2,
                                   'WKD_RATE2': 3,
                                   'WKD_RATE3': 2}, index=[0])
    # Before morning - free
    bf_morn = filter._loc_period(test_data, 5)
    assert bf_morn.RATE.values[0] == 0
    # Morning
    morn = filter._loc_period(test_data, 10)
    assert morn.RATE.values[0] == 2
    # Afternoon
    aftn = filter._loc_period(test_data, 16)
    assert aftn.RATE.values[0] == 3
    # Evening
    even = filter._loc_period(test_data, 20)
    assert even.RATE.values[0] == 2
    # After Evening
    even = filter._loc_period(test_data, 23)
    assert even.RATE.values[0] == 0


def test_select_street():
    """
    Testing selecting a single row from a large dataset
    """
    df = pd.read_csv(filter.RATE_FILE)
    info = filter.select_street(TEST_STREET_NAME, df)

    assert info.shape[0] == 1
    assert info.PARKING_TIME_LIMIT.values[0] == 120
    assert info.UNITDESC.values[0] == TEST_STREET_NAME


def	test_Street():
    """
    Testing class Street
    """
    test = filter.Street(TEST_STREET_NAME)
    assert test.name == TEST_STREET_NAME

    test.get_limit()
    assert test.limit == 2
    test.get_rate()
    assert isinstance(test.rate, pd.DataFrame)
    assert test.rate.shape[0] == 1
    assert test.get_flow_plot()

def test_flow_layer():
    """
    Testing creating flow layer
    """

    df = filter.flow_layer(datetime(2018, 12, 10, 8, 32))
    assert np.array_equal(df.columns.values, ['TIME', 'OCCUPANCY', 'UNITDESC'])
    assert df.OCCUPANCY.max() >= 0
    assert df.shape[0] == 1234

def test_rate_layer():
    """
    Testing creating rate layer
    """

    df = filter.rate_layer(datetime(2018, 12, 10, 8, 32))
    assert np.array_equal(df.columns.values, ['UNITDESC', 'RATE'])
    assert df.RATE.max() >= 0
    assert df.shape[0] == 1234

def test_recomm_layer():
    """
    Testing recommand layer
    """
    df = filter.recomm_layer((47.6062, -122.3321), datetime(2018, 12, 10, 8, 32))
    # Each property column should in 0-1 range
    for col in ['RATE', 'DISTANCE', 'OCCUPANCY', 'RECOMM']:
        assert df[col].min() == 0
        assert df[col].max() == 1
        assert df[col].dtype == 'float'
