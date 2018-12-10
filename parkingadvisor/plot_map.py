#%%
from datetime import datetime 
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import pandas as pd
import folium

import geopandas as gpd
from filter import recomm_layer
import data.clean_up as a
#%%
TIME = r'data\flow_all_streets.csv'
RATE = r'data\Rate_limit.csv'
GIS = r'data\Streets_gis.json'


gis = gpd.read_file(GIS)
#%%
df = recomm_layer(TIME,RATE,GIS,datetime(2018,12,7,16),
                 dest=(47.6062, -122.3321), factor=[0.3,0.4,0.3])
df = pd.merge(df, gis[['UNITDESC', 'geometry']], on='UNITDESC')

gdf = gpd.GeoDataFrame(df, crs= {'init' :'epsg:4326'}, geometry='geometry')

#%%
import branca

colormap = branca.colormap.linear.RdPu_05
colormap = colormap.to_step(index=['a','b','c'])
colormap.caption = 'Color'



map = folium.Map(location=[47.6062, -122.3321], tiles='cartodbpositron',
                     zoom_start=14)
folium.Marker(location=[47.6062, -122.3321]).add_to(map)
colormap.add_to(map)
#%%
style_function_2 = lambda x: {'color': colormap(x['properties']['RECOMM']),
                              'weight': 5}
#%%
folium.GeoJson(gdf.to_json(), style_function=style_function_2, name='RECOM').add_to(map)
folium.LayerControl().add_to(map)

#%%
map




#%%
map.getZoom()
#%%
