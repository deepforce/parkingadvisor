from django.shortcuts import render
from django.http import HttpResponse
import json
import geopandas
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def recommand_list(gis_data):
    pass


def show(request):
    if request.is_ajax():
        gis_data = json.loads(request.body.decode("utf8"))
        return HttpResponse(json.dumps({"msg": "Success!"}))
    else:
        return render(request, "launch_page.html")
