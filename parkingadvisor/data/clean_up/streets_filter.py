"""
Filter the streets in 'Seattle_Streets' which are studied in
'Annual_Parking_Study.csv'
"""


def subset(large, small):
    '''
    Creates a subset from a large dataset using a column elements
    in a small dataset

    Attributes:
    ------------------
    large: list (DataFrame, str)
        The large DataFrame to filter and linked column name
    small: list (DataFrame, str)
        The small dataset used to select and column name

    Returns:
    ------------------
    df_sub: DataFrame
        Subset DataFrame
    '''

    [df_large, col_large] = large
    [df_small, col_small] = small

    key = df_small[col_small].drop_duplicates()
    df_sub = df_large.loc[df_large[col_large].isin(key)]

    return df_sub
