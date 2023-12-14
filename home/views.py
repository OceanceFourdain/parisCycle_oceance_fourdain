from django.http import HttpResponse
from django.shortcuts import render
import requests
from django.views.generic import TemplateView
import json

# Get data by file json
def getDataJson():
    with open('/Users/oceance/Documents/projects/django-web-app-la-manu/pariscycle/pariscycle/templates/json/velib-disponibilite-en-temps-reel.json') as mon_fichier:
        dataJson = json.load(mon_fichier)
    #print(dataJson)
    return dataJson

# Get data by api if code error get def "getDataJson"
def getDataApi():
    all_records = []
    target_count=1469
    limit=100
    max_iterations=50
    for iteration in range(1, max_iterations + 1):
        api_params = {
            'limit': limit,
            'offset': len(all_records),
        }
        response = requests.get("https://parisdata.opendatasoft.com/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records", params=api_params)

        if response.status_code == 200:
            data = response.json()
            records = data.get('results', [])

            if len(all_records) >= target_count:
                break  # Fin de la pagination si aucun enregistrement n'est retourné

            all_records.extend(records)
        else:
            print(f"Erreur lors de la requête API. Code d'erreur : {response.status_code}")
            all_records = getDataJson()
            break
    return all_records




def home(request):
    context = {'contenu_dynamique': 'Ceci'}
    context = {
        'records': getDataJson()
    }
    return render(request, "home.html", context)
