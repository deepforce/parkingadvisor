"""
Convert a (.shp) shapefile to a GeoJSON file (.json)
"""
#%%
import shapefile
from json import dumps

def ShpToGeojson(shp_file, geojson_filename):
    """
    Attributes:
    --------------------
    shp_file:   str['*.shp']
        The shapefile filename
    geojson_filename:   str
        The given shapefile filename without extension
    
    Example:
    -------------------
    >>> ShpToGeojson(r'./Seattle_Streets/Seattle_Streets.shp', 'streets')    
    """
    # read the shapefile
    reader = shapefile.Reader(shp_file)
    #%%
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr)) 

    # write the GeoJSON file
    geojson = open(geojson_filename + '.json', "w")
    geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
    geojson.close()