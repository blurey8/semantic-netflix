from django.shortcuts import render
import json
import requests

PREFIXES = \
'''
PREFIX snr: <http://skulite.org/snr/>
PREFIX snp: <http://skulite.org/snp/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dbr: <http://dbpedia.org/resource/>
'''

local_server_url = 'http://localhost:3030/ds/query'

def get_response_from_local(query_to_send):
    try:
        response = requests.post(local_server_url, data={'query': query_to_send})
        return response.json()['results']['bindings']
    except ValueError:
        print("JSON Bermasalah atau Jena Fuseki Return 400")
        return None
    except:
        print("Jena Fuseki belum dijalankan")
        return None



def home(request):
    movies_title = []

    #query untuk mengambil semua id dan title pada ttl
    query = \
        '''
        SELECT ?id ?title
        WHERE {
            {?movies rdf:type snr:Film.}
            UNION
            {?movies rdf:type snr:Series.}
            ?movies snp:id ?id.
            ?uri snp:id ?id.
            ?uri snp:title ?title.

        }
        '''
    local_query_result = get_response_from_local(PREFIXES + query)
    for data in local_query_result:
        movies_title.append({'id':data['id']['value'],'title':data['title']['value']})

    return render(request, 'main/home.html',{'data_title':movies_title})


'''
Fungsi untuk mengambil data spesifik film
'''
def film_detail(request):

    #todo ambil data json dari spesifik film @reyhan
    #contoh query = http://127.0.0.1:8000/detail?id=80044562
    #id_film =  int(request.GET.get('id'))

    detail_film = {'uri': 'http://skulite.org/snr/A_Murder_in_the_Park',
    'title': 'A Murder in the Park',
    'director': 'Christopher S. Rech, Brandon Kimber',
    'country': 'United States',
    'dateAdded': '2017-04-28',
    'releaseYear': '2014',
    'rating': 'PG-13',
    'category': 'Documentaries',
    'description': 'This documentary excoriates a noted anti-death-penalty activist and his team, whose questionable methods got a convicted killer freed in 1999.',
    'duration': '91 min'
    }

    context = {"detail_film" : detail_film}
    return render(request, 'main/film_detail.html', context)








