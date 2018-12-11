"""
Create colormap based on rank mode
"""
import branca.colormap as cm
import folium
import geopandas as gpd
from filter import rate_layer, recomm_layer, flow_layer, link_to_gis, ev_layer


def color_bar(mode):
    """
    Create different colormap for each mode

    :param mode: 1 -- Rate, 2 -- Occupancy, 3 -- Recommanded
    :type mode: int

    :returns: color map
    :rtype: branca.Colormap
    """
    cm_name = {1: cm.linear.YlGnBu_07,
               2: cm.linear.RdPu_06,
               3: cm.linear.RdYlGn_06}
    step = {1: 6, 2: 6, 3: 5}
    colormap = cm_name[mode].to_step(step[mode])

    return colormap


def switch_layer(mode):
    """
    Switch the function to call to deal with dataset and the property
    based on the ranking mode

    :param mode: 1 -- Rate, 2 -- Occupancy, 3 -- Recommanded
    :type mode: int

    :returns: The function to deal with dataset
    :rtype: 'function'

    :returns: The property key to read
    :rtype: str
    """
    layer_func = {1: rate_layer,
                  2: flow_layer,
                  3: recomm_layer}
    prop = {1: 'RATE', 2: 'OCCUPANCY', 3: 'RECOMM'}
    return layer_func[mode], prop[mode]


class MapLayer(folium.Map):
    """
    Create a MayLAyer baseed on desticnation, parking lime
    """
    def __init__(self, date_time, dest, mode=0):
        """
        :param date_time: time of a day
        :type date_time: datetime

        :param dest: destination coordinates (longitude, latitude)
        :type dest: tuple

        """
        self.mode = mode
        self.time = date_time
        self.dest = dest

        super(MapLayer, self).__init__(location=self.dest,
                                       tiles='cartodbpositron',
                                       zoom_start=14)
        self.gdf = gpd.GeoDataFrame()
        
        if self.mode in [1, 2, 3]:
            self.colormap = color_bar(mode)
            self.style_func = None
            self.layer_func, self.prop = switch_layer(mode)
        else:
            pass
        folium.Marker(location=self.dest).add_to(self)
        self.ev = ev_layer()

    def add_layer(self):
        """
        Add the colorful layer based on the rank mode
        """
        if self.mode == 3:
            df_temp = self.layer_func(self.dest, self.time)
        elif self.mode in [1,2]:
            df_temp = self.layer_func(self.time)
        else:
            return self
        self.gdf = link_to_gis(df_temp)

        self.colormap.add_to(self)
        self.style_func = lambda x: {'color': self.colormap(x['properties'][self.prop]),
                                     'weight': 5}

        folium.GeoJson(self.gdf.to_json(), style_function=self.style_func,
                       name=self.prop).add_to(self)

        return self
    
    def add_ev_charger(self):
        """
        Add EV charging stations layers
        """
        folium.GeoJson(self.ev.to_json(), name='EV charging stations').add_to(self)

        return self
