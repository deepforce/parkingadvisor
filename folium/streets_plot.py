"""
Create a raw map with all street lines in a GeoJSON file
"""
#%%
import folium
#%%
def init(center_pos=[47.51759, -122.6016]):
    """
    Initialize the map with a given center coordinate

    Attribute:
    --------------
    center_pos:  list [long, lat]
        The coordination of the center spot. (Default: Seattle DT)
    
    Return
    ----------------
    map:    folium.Map
        An initial map
    """
    map = folium.Map(location=center_pos, tiles='Mapbox Bright',
                     zoom_start=8)
                  
    return map


def streets_plot(map, street_file, LayerName):
    """
    Add street layer to the map with a layer control

    Attribute
    -----------------
    map:    folium.Map
        The map adding the street layer
    street_file:    str
        The street geojson file
    LayerName:  str
        The name of the street layer

    Return:
    --------------------
    map:    folium.Map
        A map with a street layer
    """
    folium.GeoJson(street_file, name=LayerName).add_to(map)
    folium.LayerControl().add_to(map)

    return map

#%%
street_map = init()
streets_plot(street_map, 'streets.json', 'Seattle Streets')