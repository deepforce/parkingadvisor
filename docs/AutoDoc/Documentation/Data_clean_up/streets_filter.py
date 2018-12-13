"""
Filter the streets in 'Seattle_Streets' which are studied in
'Annual_Parking_Study.csv'
"""


def subset(large, small):
    '''
    Creates a subset from a large dataset using a column elements
    in a small dataset
    
    :param large: The large dataFrame to filter and linked column name
    :type large: list
    
    :param small: The small dataset used to select and column name
    :type small: list

    :returns: subset dataframe
    :rtype: dataframe
    '''

    [df_large, col_large] = large
    [df_small, col_small] = small

    key = df_small[col_small].drop_duplicates()
    df_sub = df_large.loc[df_large[col_large].isin(key)]

    return df_sub
