#%%
import clean_up as cln
import pandas as pd
import geopandas as gpd

#%%
# Read the Parking dataset
APSD = pd.read_csv(r".\raw_data\Annual_Parking_Study_Data.csv")
#%%
# Read the gis data of Seattle streets
fp = r".\raw_data\Seattle_Streets\Seattle_Streets.shp"
data = gpd.read_file(fp)
#%%
# Filter the gis data by parking study
street_geo = cln.subset([data,'UNITDESC'], [APSD, 'Unitdesc'])

#%%
# Save the dataframe as a GeoJSON file
cln.convert_to_geojson(street_geo, 'Streets_gis.json')