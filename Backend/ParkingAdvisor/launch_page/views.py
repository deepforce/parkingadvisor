from django.shortcuts import render
from django.http import HttpResponse
import json
import geopandas as gpd
import pandas as pd
import static.Datasets.filter as fl
import numpy as np
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import datetime
import branca
from static.Datasets.visual import color_bar


from django.views.decorators.csrf import csrf_exempt
# Create your views here.
file_time = "static/Datasets/data/flow_all_streets.csv"
file_rate = "static/Datasets/data/Rate_limit.csv"
street_geojson = "static/Datasets/data/Streets_gis.json"




def show(request):

    if request.is_ajax():
        data = json.loads(request.body.decode("utf8"))
        if "gis_lat" in data.keys():
            gis = (data['gis_lat'], data['gis_lon'])
            gis_data = gpd.read_file(street_geojson)
            now = datetime.datetime.now()

            df_recomm = fl.recomm_layer(gis, now,
                        [0.3, 0.4, 0.3])
            df_recomm = pd.merge(df_recomm, gis_data[['UNITDESC', 'geometry']], on='UNITDESC')
            gdf = gpd.GeoDataFrame(df_recomm, crs={'init': 'epsg:4326'}, geometry='geometry')
            gdf.to_file("static/Datasets/data/Streets_filtered.json", driver="GeoJSON")
            return HttpResponse(json.dumps({"msg": "Success!"}))
        elif "street_name" in data.keys():
            unitdesc = data['street_name']
            street = fl.Street(street_name = unitdesc)
            df = street.get_rate()
            fig = street.get_flow_plot()
            fig.savefig("static/images/parkingfig/info.svg", bbox_inches='tight')
            return HttpResponse(json.dumps({"street": street.get_name(), "limit": street.get_limit(),
                                        "tables": df.to_html(classes='data', index = False, header=False), "titles": str(df.columns.values)}))
        else:
            evname = data['ev_name']
            ev_charger = fl.EStation(station_name = evname)
            return HttpResponse(json.dumps({"address": ev_charger.address, "code": ev_charger.code,
                                        "phone": ev_charger.phone, "NEMA520": ev_charger.NEMA520,
                                        "J1772": ev_charger.J1772, "CHADEMO": ev_charger.CHADEMO,
                                        "TESLA": ev_charger.TESLA, "level1": ev_charger.level1,
                                        "level2": ev_charger.level2, "dc": ev_charger.dc}))
    else:
        mode = 3
        colormap = color_bar(mode)
        colorlist = []
        colorbar = []

        step = {1: 6, 2: 6, 3: 5}
        index = np.around(np.linspace(0,1,step[mode]+1),1)
        for i in range(0, len(index)-1):
            colorbar.append(colormap(index[i]+0.0001))
        # print(colorbar)
        street_df = gpd.read_file("static/Datasets/data/Streets_filtered.json")
        for k in street_df['RECOMM']:
            colorlist.append(colormap(k))
        return render(request, "launch_page.html", {"colorlist": json.dumps(colorlist), "colorbar": json.dumps(colorbar),
                                                    "grades": json.dumps(index.tolist())})






