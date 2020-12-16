from django.shortcuts import render

from .utils.constants import *
from .utils.helpers import (
    get_all_films,
    get_film_object_dbpedia,
    get_film_object_wikidata,
    get_film_detail_local,
    get_film_detail_dbpedia,
    get_film_detail_wikidata
)


'''
Fungsi untuk mengambil data spesifik film
'''
def home(request):
    movies_title = []

    query_result = get_all_films()
    for data in query_result:
        movies_title.append({'id':data['id']['value'],'title':data['title']['value']})

    return render(request, 'main/home.html',{'data_title':movies_title})

'''
Fungsi untuk mengambil data spesifik film
'''
def film_detail(request):
    film_details = {}
    film_id = request.GET.get('id')
    
    local_query_result = get_film_detail_local(film_id)

    dbpedia_object_name = get_film_object_dbpedia(film_id)
    dbpedia_query_result = get_film_detail_dbpedia(dbpedia_object_name)
    
    wikidata_object_name = get_film_object_wikidata(film_id)
    wikidata_query_result = {}
    
    if wikidata_object_name:
        wikidata_query_result = get_film_detail_wikidata(wikidata_object_name)
    
    if dbpedia_query_result == {} :
        # Jika DBPedia hasilnya kosong, maka data lokal ditambah data wikidata    
        film_details.update(local_query_result)
        film_details.update(wikidata_query_result)
    
    else :
        # Jika DBPedia ada isinya, maka data lokal ditambah data dbpedia    
        film_details.update(local_query_result)
        film_details.update(dbpedia_query_result)
    
    if "image" in wikidata_query_result:
        film_details.update(wikidata_query_result['image'])
    
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
