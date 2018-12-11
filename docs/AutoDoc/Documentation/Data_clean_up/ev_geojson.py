"""
Reads the Washington State EV charger stations dataset and creates
a DataFrame of all Seattle stations with necessary information.
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import Point


def all_type(dataframe):
    """
    Find all availble EV connector types in column ['EV Connector Types']

    :param dataframe: The dataframe to deal
    :type dataframe: dataframe
        
    :returns: A list of all availible connector types
    :rtype: dict
    """

    type_dict = {}
    for item in dataframe['EV Connector Types']:
        # splits the long string of several EV connector types
        splt_list = item.split(' ')
        # counts the types in the entire DataFrame
        for c_type in splt_list:
            if c_type in type_dict:
                type_dict[c_type] += 1
            else:
                type_dict[c_type] = 1

    return type_dict


def ev_level_tf(dataframe, col_ori, col_new):
    """
    Creates new columns to describe each station charging levels

    :param dataframe: The dataframe to deal
    :type dataframe: dataframe

    :param col_ori: The original column name of the EV Levels
    :type col_ori: str

    :param col_new: The name of new column
    :type col_new: str
        
    :returns: The dataFrame with new columns
    :rtype: dataframe
    """

    dataframe[col_new] = np.isfinite(dataframe[col_ori])

    return dataframe


def ev_connector_tf(dataframe, type_list):
    """
    Creates new columns to describe each station connector types

    :param dataframe: the dataframe to deal with
    :type dataframe: dataframe

    :param type_list: all connector types
    :type type_list: list
        
    :returns: The dataFrame with new columns
    :rtype: dataframe
    """

    # splits the long string
    for connector in type_list:
        dataframe[connector] = dataframe['EV Connector Types'].str.contains(connector, regex=False)

    return dataframe


def convert_to_geojson(dataframe, filename):
    """
    Saves a DataFrame as GeoJSON

    :param dataframe: the dataframe to save
    :type dataframe: dataframe

    :param filename: The given filename
    :type filename: str
    """
    if not 'geometry' in dataframe.columns:
        dataframe['geometry'] = dataframe.apply(lambda z: Point(z.Longitude, z.Latitude), axis=1)
        dataframe.drop(['Latitude', 'Longitude'], axis=1)

    dataframe_geo = gpd.GeoDataFrame(dataframe)
    geojson = open(filename, "w")
    geojson.write(dataframe_geo.to_json(indent=2) + '\n')
    geojson.close()
