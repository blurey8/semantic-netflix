from django.shortcuts import render
from .utils.constants import FUSEKI_URL, PREFIXES

from .utils.helpers import (get_data_from_local, get_data_from_remote, 
get_film_object_from_id, get_combined_individual_film_detail)

'''
Fungsi untuk mengambil data spesifik film
'''
def home(request):
    movies_title = []

    #Query untuk mengambil semua id dan title pada ttl
    query = \
    '''
    SELECT ?id ?title WHERE {
        {?movies rdf:type snr:Film.}
        UNION
        {?movies rdf:type snr:Series.}
        ?movies snp:id ?id.
        ?uri snp:id ?id.
        ?uri snp:title ?title.
    }
    '''

    local_query_result = get_data_from_local(query)
    for data in local_query_result:
        movies_title.append({'id':data['id']['value'],'title':data['title']['value']})

    return render(request, 'main/home.html',{'data_title':movies_title})

'''
Fungsi untuk mengambil data spesifik film
'''
def film_detail(request):

    #Query untuk ambil data json dari spesifik film
    id_film =  request.GET.get('id')
    id_formatted = '\"{}\"'.format(id_film)

    query_local = \
    '''
    SELECT * WHERE { 
        ?uri snp:id %s ;
        snp:title ?title ;
        snp:director ?director ;
        snp:country ?country ;
        snp:dateAdded ?dateAdded ;
        snp:releaseYear ?releaseYear ;
        snp:rating ?rating ;
        snp:category ?category ;
        snp:description ?description ;
        OPTIONAL {
            ?uri snp:duration ?duration .
        }
        OPTIONAL {
            ?uri snp:numOfSeasons ?season .
        }
    }
    ''' % (id_formatted)

    film_details = {}
    local_query_result = get_data_from_local(query_local)[0]

    # Menyimpan hasil query data lokal dalam bentuk dictionary
    for key in local_query_result:
        film_details[key] = local_query_result[key]['value']

    film_object_name = get_film_object_from_id(id_film)

    query_remote = \
    '''
    SELECT * WHERE {
        OPTIONAL {
            dbr:%s dbo:distributor ?distributor .
        }
        OPTIONAL {
            dbr:%s dbo:producer ?producer .
        }
        OPTIONAL {
            dbr:%s foaf:homepage ?homepage .
        }
    }
    ''' % (film_object_name, film_object_name, film_object_name)

    remote_query_result = get_data_from_remote(query_remote)
    
    # Menyimpan hasil query data remote dalam bentuk dictionary
    for row in remote_query_result:
        film_details['distributor'] = row.distributor
        film_details['producer'] = row.producer
        film_details['homepage'] = row.homepage

    print(film_details)

    context = {"detail_film" : film_details} 

    return render(request, 'main/film_detail.html', context)

'''
Fungsi untuk melakukan pencarian film berdasarkan judul
'''
def film_search(request):
    
    #TODO: Cari film berdasarkan judul -> Reyhan
    #TODO: Filter Pencarian -> Reyhan
    #Contoh query judul = http://127.0.0.1:8000/search?title=murder%20in%20%20park
    
    title_film = request.GET.get('title').lower()
    title_formatted = '\"{}\"'.format(title_film)

    pass