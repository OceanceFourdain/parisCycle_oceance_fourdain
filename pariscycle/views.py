from django.http import HttpResponse
from django.shortcuts import render
import requests
import numpy as np
import folium
from folium.plugins import MarkerCluster, Search
from django.views.generic import TemplateView
import json

def index(request):
    return render(request, "index.html")
# Get data by file json
def getDataJson(nameFile):
    #/Users/oceance/Documents/projects/django-web-app-la-manu/pariscycle/pariscycle/templates/json/velib-disponibilite-en-temps-reel.json'
    with open(f"/Users/oceance/Documents/projects/django-web-app-la-manu/pariscycle/pariscycle/templates/json/{nameFile}.json") as mon_fichier:
        dataJson = json.load(mon_fichier)
    #print(dataJson)
    return dataJson

# Get data by api if code error get def "getDataJson"
def getDataApi(nameOption, counterApi):
    all_records = []
    target_count=counterApi
    limit=100
    max_iterations=50
    for iteration in range(1, max_iterations + 1):
        api_params = {
            'limit': limit,
            'offset': len(all_records),
        }
        if iteration <= 50:
            response = requests.get(f"https://parisdata.opendatasoft.com/api/explore/v2.1/catalog/datasets/{nameOption}/records", params=api_params)

            if response.status_code == 200:
                data = response.json()
                records = data.get('results', [])

                if len(all_records) >= target_count:
                    break  # Fin de la pagination si aucun enregistrement n'est retourné

                all_records.extend(records)
            else:
                print(f"Erreur lors de la requête API. Code d'erreur : {response.status_code}")
                all_records = getDataJson(nameOption)
                break
        else:
            all_records = getDataJson(nameOption)
    return all_records

# Create cardMarker and send params array data
def cardMarker(data):
    html = f"""
        <!-- Header and footer -->
        <div class="card text-center">
            <div class="card-header">{data['name']}</div>
            <div class="card-body">
                <p class="card-text">Capacité de la station {data['capacity']}</p>
                <p class="card-text">Nombre de bornes disponible {data['borneDispo']}</p>
                <p class="card-text">Vélo mécaniques disponible {data['mechanical']}</p>
                <p class="card-text">Vélo électrique disponible {data['ebike']}</p>
            </div>
            <div class="card-footer fs-sm text-muted"><span>{data['nom_arrondissement_communes']}</span> <span>{data['duedate']}</span></div>
        </div>
        """
    return html
    
#View maps
def maps(request):
    ### Get Data ###
    data_station = getDataApi("velib-disponibilite-en-temps-reel", 1469)
    ### Create maps folium  ###
    attr = (
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
    'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    # Create map 
    m = folium.Map([48.852743, 2.346769], tiles=None, attr=attr, zoom_start=10)

    # If you want get the user device position after load the map, set auto_start=True
    folium.TileLayer(
        name="Plan IGN", 
        tiles="https://wxs.ign.fr/decouverte/geoportail/wmts?&REQUEST=GetTile&SERVICE=WMTS&VERSION=1.0.0&TILEMATRIXSET=PM&layer=GEOGRAPHICALGRIDSYSTEMS.PLANIGNV2&STYLE=normal&FORMAT=image/png&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}", 
        attr=attr
    ).add_to(m)
    folium.plugins.LocateControl().add_to(m)
    folium.plugins.LocateControl(auto_start=False).add_to(m)
    # Create cluster and add marker
    mcg = MarkerCluster(control=False)
    m.add_child(mcg)

    g1 = folium.plugins.FeatureGroupSubGroup(mcg, "Station de vélo")
    m.add_child(g1)

    for item in data_station:
        data = {'stationcode': item['stationcode'],'name': item['name'], 'borneDispo': item['numdocksavailable'], 'capacity': item['capacity'], 'mechanical': item['mechanical'], 'ebike': item['ebike'], 'nom_arrondissement_communes': item['nom_arrondissement_communes'], 'duedate': item['duedate']}
        
        popup=cardMarker(data)
        
        pushpin = folium.features.CustomIcon('/Users/oceance/Documents/projects/django-web-app-la-manu/pariscycle/pariscycle/static/icon/icon_velo.png', icon_size=(30,40))
        folium.Marker(
            location=[item['coordonnees_geo']['lat'], item['coordonnees_geo']['lon']],
            tooltip="Information",
            popup=folium.Popup(popup, max_width=500, max_height=300),
            icon=pushpin,
            localize=True
        ).add_to(g1)
    #folium.RegularPolygonMarker(location=[51.5, -0.25], popup=popup).add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    m=m._repr_html_() #updated`
    context = {
        'map': m
    }
    return render(request, "maps.html", context)

#View all data in table
def parisdata(request):
    context = {
        'records': getDataJson()
    }
    return render(request, "parisdata.html", context)
