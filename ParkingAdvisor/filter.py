"""
This module contains all methods to filter the data to visualization
and calculation.
"""
import pandas as pd
from scipy.interpolate import interp1d
import numpy as np
import geopandas as gpd
from geopy.distance import geodesic


# Calculations processing on clean datasets
def _model_flow(d_flow_hour): # DONE
    '''
    Smooth the occupancy profile by interpolation ('cubic') to fix the
    missing data point issue and provide pretty profile graphs later

    Attributes:
    -----------------
    d_flow_discrete: DataFrame
        The hourly flow data of certain street

    Return:
    -----------------
    d_flow: DataFrame
        Smoothed flow dataframe by interpolation
    '''
    # Cubic interpolation
    f_flow = interp1d(
        d_flow_hour['HOUR'], d_flow_hour['OCCUPANCY'], kind='cubic',
        fill_value='extrapolate')

    t_new = np.linspace(8, 24, num=161, endpoint=True)
    flow = f_flow(t_new)
    # Create smoothed flow DataFrame
    d_flow = pd.DataFrame({'TIME': t_new, 'OCCUPANCY': flow})
    # d_flow['TIME'] = d_flow['TIME'].astype('category')

    d_flow.OCCUPANCY.loc[d_flow.OCCUPANCY < 0] = 0

    return d_flow


def _create_smooth_flow_file(file_flow): # DONE
    '''
    Generates the parking utilities of all streets by interpolation
    and save a .csv file

    Attributes:
    -------------------
    file_flow: file
        The entire flow dataset file

    Return:
    --------------------
    data_hour: DataFrame
        All streets smoothed occupancy
    '''

    df_flow = pd.read_csv(file_flow, index_col=0)
    df_flow['UNITDESC'] = df_flow['UNITDESC'].astype('category')

    # Create an empty dataframe to store smoothed flow data
    num = len(df_flow['UNITDESC'].cat.categories)

    data_time = pd.DataFrame(pd.np.empty((161*num, 2)) * pd.np.nan,
                             columns=['TIME', 'OCCUPANCY'])
    new_index = np.repeat(df_flow['UNITDESC'].cat.categories, 161)

    # Group by street name as index
    idx_start = 0
    for cat in df_flow['UNITDESC'].cat.categories:
        d_street = df_flow.loc[df_flow['UNITDESC'] == cat]
        d_smooth = _model_flow(d_street)

        data_time.iloc[idx_start:idx_start+161].values[:] = d_smooth.values[:]

        idx_start += 161

    data_time['UNITDESC'] = new_index
    data_time.to_csv(r'.\data\flow_all_streets.csv')

    return data_time


def _loc_period(df_selected_day, hour): # DONE
    """
    Determine the given hour number in which time section
    and get the corresponding rate

    Attributes
    ---------------------
    df_selected_day: DataFrame
        the rate info dataframe with columns [key timepoint (n), rate_list (n-1)]
        for each section
        NOTE
        -----------time1--------time2--------time3----------time4(n)----------
        |----SEC0----|----SEC1----|----SEC2---|-----SEC3-----|----SEC4----|
                     |   --------------input---------------  |
    hour: int
        the number of datetime hour

    Return:
    -------------------
    df_rate: DataFrame
        the rate for all streets at the given time
    """
    # get the key timepoint number
    n_time = int(df_selected_day.shape[1] / 2)

    # Insert the rate of free timezone
    df_selected_day.insert(n_time + 1, 'SEC0', 0)
    df_selected_day['LAST_SEC'] = 0

    # Fill NaN by np.inf
    df_selected_day = df_selected_day.fillna(np.inf)

    # Initial the streets and rate array
    streets = np.array([])
    rate = np.array([])

    # Group by the timezone condition
    group = df_selected_day.groupby(df_selected_day.columns[1: n_time + 1].values.tolist())
    for key, value in dict(list(group)).items():

        # Get the array of timepoints. (e.g. [8, 11, 17, 20])
        # And substrate the given hour number (e.g. [0, 3, 9, 12] when hour=8)
        sub = np.array(key)-hour

        # Count the non-positive values, which refers ot the section num
        # (e.g. sec = 1. So hour=8 in SEC1)
        sec = (sub <= 0).sum()

        temp1 = value['UNITDESC'].values
        temp2 = value.iloc[:, n_time + sec + 1].values
        streets = np.append(streets, temp1)
        rate = np.append(rate, temp2)
    df_rate = pd.DataFrame({'UNITDESC': streets, 'RATE': rate})
    df_rate.replace(to_replace=np.inf, value=0, inplace=True)

    return df_rate


def _calc_distance(street_geojson, gis_data): # DONE
    """
    Calculates the distance from a given location to all streets
    (midpoint of linestring)

    Attributes:
    -------------------
    street_geojson: JSON file
        The GeoJSON file of all streets (i.e. Streets_gis.json)
    gis_data:   list (lat, long)
        The given point coordinate

    Returns:
    --------------------
    df_dist: dataframe
        a DataFrame of distance of a given point to all streets
    """
    street_df = gpd.read_file(street_geojson)
    coord = street_df.geometry.apply(lambda p: p.coords) # (long, lat)

    # Calculates the midpoint of each street line
    m_list = [] # (lat, long)
    for i in coord:
        m_list.append(((i[0][1] + i[1][1])/2, (i[0][0] + i[1][0])/2))

    # Calculates the distance
    distance = []
    for i in m_list:
        distance.append(geodesic(gis_data, i).miles)

    street_df['DISTANCE'] = distance
    df_dist = street_df[['UNITDESC', 'DISTANCE']]

    return df_dist


def read_street_file(file_flow, file_rate, street_name): # DONE
    '''
    Select the parking utilities of a certain street
    for sider bar display

    Attributes:
    -------------------
    file_flow: file
        The entire flow file
    file_rate: file
        The entire rate file
    street_name: str
        The name of the certain street

    Return:
    --------------------
    df_flow: DataFrame
        The occupancy per hour of the day
    df_rate: Series
        The rate info of the street

    Examples:
    -------------------
    >>> df_flow, df_rate = select_street(
            file_flow='..\\data\\Occupancy_per_hour.csv',
            file_rate='..\\data\\Rate_limit.csv',
            street_name='10TH AVE BETWEEN E PIKE ST AND E PINE ST')

    >>> df_flow.head()
    >>>    TIME	OCCUPANCY
        0	8.0	0.493407
        1	8.1	0.503239
        2	8.2	0.513154
        3	8.3	0.523411
        4	8.4	0.534272
    >>> df_rate
    '''

    df_flow = pd.read_csv(file_flow, index_col=0)
    df_flow = df_flow['UNITDESC'].astype('category')
    street = df_flow.loc[df_flow.UNITDESC == street_name]
    df_flow_hour = pd.DataFrame({'HOUR': street['HOUR'],
                                 'OCCUPANCY': street['OCCUPANCY']})
    df_flow = _model_flow(df_flow_hour)

    df_rate = pd.read_csv(file_rate, index_col=0)
    df_flow = df_flow['UNITDESC'].astype('category')
    df_rate = df_rate.loc[df_rate.UNITDESC == street_name]

    return df_flow, df_rate


# Folium map plot layers
def flow_layer(file_time, date_time): # DONE
    """
    Generate a dataframe of occupancy for all streets at a specific
    time point for folium map plot

    Attribute
    ----------------
    file_time: file
        The path of the raw file which containing all smoothed
        occupancy data (i.e. 'flow_all_streets.csv')
    date_time:   `datatime` object
        The start time of parking

    Return
    -----------------
    df_flow:    DataFrame
        A dataframe containing occupancy at the time point
    """
    # Round the time decimal to 1 digit

    time_float = date_time.hour + date_time.minute/60.0
    time_float = round(time_float, 1)

    d_entire = pd.read_csv(file_time, index_col=0)

    # Change columns dtype to accelerate
    for col in ['UNITDESC', 'TIME']:
        d_entire[col] = d_entire[col].astype('category')

    df_flow = d_entire.loc[np.isclose(d_entire[col], time_float)]

    return df_flow


def rate_layer(file_rate, date_time): # DONE
    """
    Generate a dataframe of parking rate for all streets at a specific
    datetime

    Attributes:
    -----------------
    file_rate: file
        The entire rate file (i.e. 'Rate_limit.csv')
    date_time: `datatime` Object
        the start time of parking

    Returns:
    -------------------
    df_rate
    """
    raw = pd.read_csv(file_rate)
    raw.apply(pd.to_numeric, errors='ignore')

    day = date_time.isoweekday()
    hour = date_time.hour

    # SUN - free
    if day == 7:
        df_rate = pd.DataFrame({'UNITDESC': raw.UNITDESC, 'RATE': 0})
    # SAT
    elif day == 6:
        cols = ['UNITDESC', 'SAT_START1', 'SAT_END1', 'SAT_END2', 'SAT_END3',
                'SAT_RATE1', 'SAT_RATE2', 'SAT_RATE3']
        df_rate = _loc_period(raw.loc[:, cols], hour)
    # WKD
    else:
        cols = ['UNITDESC', 'WKD_START1', 'WKD_END1', 'WKD_END2', 'WKD_END3',
                'WKD_RATE1', 'WKD_RATE2', 'WKD_RATE3']
        df_rate = _loc_period(raw.loc[:, cols], hour)

    return df_rate


def recomm_layer(file_time, file_rate, street_geojson,
                 date_time, dest, factor):
    """
    Generates a dataframe with recommanded score for all streets

    Attributes:
    -------------------
    file_time: file
        The path of the raw file which containing all smoothed
        occupancy data (i.e. 'flow_all_streets.csv')
    file_rate: file
        The entire rate file (i.e. 'Rate_limit.csv')
    street_geojson: JSON file
        The GeoJSON file of all streets (i.e. Streets_gis.json)
    date_time: `datetime` object
        The start time point
    dest: tuple (lat,long)
        The destination coordinates
    factor: list (order: 'RATE', 'FLOW', 'DISTANCE')
        The score factor to calculate recommanded score

    Returns:
    -------------------
    df_recomm:  DataFrame
        dataframe of recommanded scores
    """

    df_rate = rate_layer(file_rate, date_time)
    df_flow = flow_layer(file_time, date_time)
    df_dist = _calc_distance(street_geojson, dest)

    df_recomm = pd.merge(df_rate, df_flow, on='UNITDESC')
    df_recomm = pd.merge(df_recomm, df_dist, on='UNITDESC')
    df_recomm = df_recomm.drop(['TIME'], axis=1)
    df_recomm['RECOMM'] = np.nan
    df_recomm['DISTANCE'] = df_recomm['DISTANCE'].apply(np.log10)

    df_recomm['RECOMM'].values[:] = np.dot(df_recomm.iloc[:, 1:-1].values, factor)[:]
    df_recomm['RECOMM'] = - df_recomm['RECOMM']

    return df_recomm
