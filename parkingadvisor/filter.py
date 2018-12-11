"""
This module contains all methods to filter the data to visualization
and calculation.
"""

import pkg_resources
from datetime import datetime

import pandas as pd
from scipy.interpolate import interp1d
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from geopy.distance import geodesic


PACKAGE_NAME = __name__
DATA_PATH = pkg_resources.resource_filename(PACKAGE_NAME, 'data/')

RATE_FILE = DATA_PATH + 'Rate_limit.csv'
_FLOW_RAW = DATA_PATH + 'Occupancy_per_hour.csv'
FLOW_FILE = DATA_PATH + 'flow_all_streets.csv'
GIS_FILE = DATA_PATH + 'Streets_gis.json'
EV_FILE = DATA_PATH + 'EV Charger.json'

_INTERPOLATION_NUM = 241
RECOMM_FACTOR = (0.3, 0.4, 0.3)

# Calculations processing on clean datasets
def _model_flow(d_flow_hour):
    '''
    Smooth the occupancy profile by interpolation ('cubic') to fix the
    missing data point issue and provide pretty profile graphs later

    :param d_flow_hour: The hourly flow data of certain street
    :type d_flow_hour: dataframe

    :returns: Smoothed flow dataframe by interpolation
    :rtype: dataframe
    '''
    # Cubic interpolation
    f_flow = interp1d(
        d_flow_hour['HOUR'], d_flow_hour['OCCUPANCY'], kind='cubic',
        fill_value='extrapolate')

    t_new = np.linspace(0, 24, num=_INTERPOLATION_NUM, endpoint=True)
    flow = f_flow(t_new)
    # Create smoothed flow DataFrame
    d_flow = pd.DataFrame({'TIME': t_new, 'OCCUPANCY': flow})
    d_flow.OCCUPANCY.loc[d_flow.OCCUPANCY < 0] = 0

    return d_flow


def _create_smooth_flow_file(file_flow=_FLOW_RAW):
    '''
    Generates the parking utilities of all streets by interpolation
    and save a .csv file

    :param file_flow: The entire flow dataset file
    :type file_flow: str

    :returns: The entire flow dataset file
    :rtype: dataframe
    '''

    df_flow = pd.read_csv(file_flow, index_col=0)
    df_flow['UNITDESC'] = df_flow['UNITDESC'].astype('category')

    # Create an empty dataframe to store smoothed flow data
    num = len(df_flow['UNITDESC'].cat.categories)

    data_time = pd.DataFrame(pd.np.empty((_INTERPOLATION_NUM * num, 2)) * pd.np.nan,
                             columns=['TIME', 'OCCUPANCY'])
    new_index = np.repeat(df_flow['UNITDESC'].cat.categories, _INTERPOLATION_NUM)

    # Group by street name as index
    idx_start = 0
    for cat in df_flow['UNITDESC'].cat.categories:
        d_street = df_flow.loc[df_flow['UNITDESC'] == cat]
        d_smooth = _model_flow(d_street)

        data_time.iloc[idx_start:(idx_start + _INTERPOLATION_NUM)].values[:] = d_smooth.values[:]

        idx_start += _INTERPOLATION_NUM

    # Save the smooth file in data folder
    data_time['UNITDESC'] = new_index
    data_time.to_csv(r'.\data\flow_all_streets.csv')

    return data_time


def _loc_period(df_selected_day, hour):
    """
    Determine the given hour number in which time section
    and get the corresponding rate.
    NOTE
        -----------time1--------time2--------time3----------time4(n)----------
        |----SEC0----|----SEC1----|----SEC2---|-----SEC3-----|----SEC4----|
                     |   --------------input---------------  |

    :param df_selected_day: the rate info dataframe with columns [key timepoint (n), rate_list (n-1)] 
                            for each section
    :type df_selected_day: dataframe

    :param hour: the number of datetime hour
    :type hour: int

    :returns: the rate for all streets at the given time
    :rtype: dataframe
    """
    if 'SEC0' not in df_selected_day.columns:
        # Get the key timepoint number
        n_time = int(df_selected_day.shape[1] / 2)
        # Insert the rate of free timezone
        df_selected_day.insert(n_time + 1, 'SEC0', 0)
        df_selected_day['LAST_SEC'] = 0
    else:
        # Have inserted the free time region columns
        n_time = int(df_selected_day.shape[1] / 2) -1

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
    df_rate.RATE.astype('float')

    return df_rate


def _calc_distance(gis_data, street_geojson=GIS_FILE):
    """
    Calculates the distance from a given location to all streets
    (midpoint of linestring)

    :param gis_data: The given point coordinate, including longitude and latitude
    :type gis_data: list

    :param street_geojson: The GeoJSON file of all streets (i.e. Streets_gis.json)
    :type street_geojson: str

    :returns: a dataframe of distance of a given point to all streets
    :rtype: dataframe
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


def select_street(street_name, df_entire):
    """
    Select a specific street info from entire dataframe

    :param street_name: The given street name
    :type street_name: str

    :param df_entire: The dataframe containing all streets
    :type df_entire: dataframe

    :returns: info of specific street name
    :rtype: dataframe
    """

    info = df_entire.loc[df_entire['UNITDESC'] == street_name]
    return info


def plot_flow(df_smooth_flow):
    """
    Plot the flow figure for a single street

    :param df_smooth_flow: The smoothed flow data of a dingle street
    :type df_smooth_flow: dataframe

    :returns: a figure containing the info of a dataframe
    :rtype: matplotlib.pyplot.Figure
    """
    time = df_smooth_flow['TIME']
    flow = df_smooth_flow['OCCUPANCY']

    fig = plt.figure(figsize=(4, 2.5), frameon=False, facecolor=None)
    plt.fill_between(time, flow, alpha=0.5, edgecolor='#1B5C99',
                     facecolor='#84B5D1', lw=2)

    # Change tick labels
    plt.xticks([8, 12, 16, 20, 24], ['8 AM', '12 PM', '4 PM', '8 PM', '12 AM'])
    plt.yticks([0, 0.5, 1], ['0', '50', '100 %'])
    # Set axis limit
    plt.xlim([8, 24])
    plt.ylim([0, 1])
    # Delete y axis
    ax = plt.gca()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Only show labels on left spines
    ax.tick_params(left=False, labelleft=True, axis='both', which='major', labelsize=12)
    ax.tick_params(axis='x', pad=8)
    ax.xaxis.set_ticks_position('bottom')
    # Show girds
    plt.grid(color='dimgrey', alpha=0.5)

    return fig


class Street():
    """
    The class `Street` contains all information of a on-street parking
    spot for future details display.

    Attributes:
    ---------------------
    name:   The street name
    plot:   Occupancy over time figure
    rate:   Parking rate table
    limit:  Parking limit (in hour)
    """

    def __init__(self, street_name):
        """
        :param street_name: The given street name
        :type street_name: str
        """
        self.name = street_name

        df_flow = pd.read_csv(FLOW_FILE, index_col=0)
        self._flow_df = select_street(self.name, df_flow)

        df_rate = pd.read_csv(RATE_FILE, index_col=0).fillna(0)
        self._rate_df = select_street(self.name, df_rate)
        self.rate = pd.DataFrame(columns=['DAYS', 'SEC1', 'SEC2', 'SEC3'])
        
        self.limit = 0

    def get_name(self):
        "Street name"
        return self.name

    def get_rate(self):
        "Get rate table"
        time_points = [int(self._rate_df.values[0][i]) for i in [2, 3, 5, 6, 8, 9,
                                           11, 12, 14, 15, 17, 18]]
        rate = [self._rate_df.values[0][i] for i in [1, 4, 7, 10, 13, 16]]
        # Create a list to store key timepoint in `str` and 12-hour clock
        timepoint_text = []
        for hour in time_points:
            # Convert 24h to 12h
            if hour == 0:
                hour_new = '-'
            else:
                hour_new = datetime.strptime(str(hour), '%H').strftime("%I %p").lstrip('0')
            timepoint_text.append(hour_new)
        self.rate['DAYS'] = ['','WKD','SAT']

        time_label = [timepoint_text[2 * i]+'-'+ timepoint_text[2 * i + 1] for i in range(6)]
        self.rate.iloc[0, 1:].values[:] = time_label[:3]        
        self.rate.iloc[1, 1:].values[:] = rate[:3]
        self.rate.iloc[2, 1:].values[:] = rate[3:]

        return self.rate

    def get_limit(self):
        "Get parking limit in hour"
        self.limit = self._rate_df.iloc[0, -1]/60 # convert into hour
        return self.limit

    def get_flow_plot(self):
        "Get the flow analysis figure"
        self.plot = plot_flow(self._flow_df)
        return self.plot


# Folium map plot layers
def flow_layer(date_time, file_time=FLOW_FILE):
    """
    Generate a dataframe of occupancy for all streets at a specific
    time point for folium map plot

    :param date_time: The start time of parking
    :type date_time: `datatime` 

    :param file_time: The path of the raw file which containing all smoothed
                        occupancy data (i.e. 'flow_all_streets.csv')
    :type file_time: str

    :returns: A dataframe containing occupancy at the time point
    :rtype: dataframe
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


def rate_layer(date_time, file_rate=RATE_FILE):
    """
    Generate a dataframe of parking rate for all streets at a specific
    datetime

    :param date_time: the start time of parking
    :type date_time: `datatime`

    :param file_rate: The entire rate file (i.e. 'Rate_limit.csv')
    :type file_rate: str

    :returns: a dataframe containing all the info of the layer
    :rtype: dataframe
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


def recomm_layer(dest, date_time, factor=RECOMM_FACTOR):
    """
    Generates a dataframe with recommanded score for all streets

    :param dest: The destination coordinates
    :type dest: tuple-like (lat,long)

    :param date_time: The start time point
    :type date_time: `datetime`

    :param factor: The score factor to calculate recommanded score
    :type factor: list

    :returns: dataframe of recommanded scores
    :rtype: dataframe
    """
    # Get all properties
    df_rate = rate_layer(date_time)
    df_flow = flow_layer(date_time)
    df_dist = _calc_distance(dest)

    # Merge into one DataFrame
    df_recomm = pd.merge(df_rate, df_flow, on='UNITDESC')
    df_recomm = pd.merge(df_recomm, df_dist, on='UNITDESC')
    df_recomm = df_recomm.drop(['TIME'], axis=1)

    # Normalize each column
    df_recomm['DISTANCE'] = df_recomm['DISTANCE'].apply(np.log10)

    df_recomm.iloc[:, 1:4] = df_recomm.iloc[:, 1:4].apply(
        lambda x: (x - np.min(x))/(np.max(x) - np.min(x)) if x.any() else x)

    df_recomm['RECOMM'] = np.nan
    df_recomm['RECOMM'].values[:] = np.dot(
        df_recomm.iloc[:, 1:-1].values, factor)[:]

    # Normalize the recommand score
    r_max = np.max(df_recomm['RECOMM'])
    r_min = np.min(df_recomm['RECOMM'])
    df_recomm['RECOMM'] = df_recomm['RECOMM'].apply(
        lambda x: (r_max - x)/(r_max - r_min))

    return df_recomm


def link_to_gis(df_properties, street_geojson=GIS_FILE):
    """
    Add GIS info to properties dataframe

    :param df_properties: the dataframe of properties
    :type df_properties: `datatime`

    :param street_geojson: the JSON file constaining street info
    :type street_geojson: str

    :returns: a dataframe linked to gis
    :rtype: GeoPandas.DataFrame
    """

    gis = gpd.read_file(street_geojson)
    df_properties = pd.merge(df_properties, gis[['UNITDESC', 'geometry']],
                             on='UNITDESC')
    df_gis = gpd.GeoDataFrame(df_properties, crs={'init' :'epsg:4326'},
                              geometry='geometry')

    return df_gis


def ev_layer(ev_gis=EV_FILE):
    """
    Read the EV charging stations datafile and convert into a
    GeoPandas.DataFrame
    
    :param ev_gis: the JSON file constaining layer info
    :type ev_gis: str

    :returns: a dataframe of the layer
    :rtype: GeoPandas.DataFrame
    """
    df_ev = gpd.read_file(ev_gis)
    return df_ev


def select_station(staion_name, df_entire):
    """
    Select a specific street info from entire dataframe

    :param street_name: The given street name
    :type street_name: str

    :param df_entire: The dataframe containing all streets
    :type df_entire: dataframe

    :returns: a dataframe containing specific station
    :rtype: dataframe
    """

    info = df_entire.loc[df_entire['Station Name'] == staion_name]
    return info


class EStation():
    """
    The class `EStation` contains all information of a EV charging station
    for future details display.

    Attributes:
    ---------------------
    name:   The street name
    plot:   Occupancy over time figure
    rate:   Parking rate table
    limit:  Parking limit (in hour)
    """

    def __init__(self, station_name):
        """
        :param station_name: The given station name
        :type station_name: str
        """

        self.name = station_name

        df_ev = gpd.read_file(EV_FILE)
        ev_row = select_station(self.name, df_ev)

        self.address = ev_row['Street Address'].values[0]
        self.code = ev_row['ZIP'].values[0]
        self.phone = ev_row["Station Phone"].values[0]

        self.level1 = ev_row['Level 1'].values[0]
        self.level2 = ev_row['Level 2'].values[0]
        self.dc = ev_row['DC Fast'].values[0]

        self.NEMA520 = ev_row['NEMA520'].values[0]
        self.J1772 = ev_row['J1772'].values[0]
        self.J1772COMBO = ev_row['J1772COMBO'].values[0]
        self.CHADEMO = ev_row['CHADEMO'].values[0]
        self.TESLA = ev_row['TESLA'].values[0]
