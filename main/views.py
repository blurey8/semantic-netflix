from django.shortcuts import render
from .utils.helpers import get_film_data

def home(request):
    #todo ambil semua id dan nama dari film @reyhan

    return render(request, 'main/home.html')

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

'''
Fungsi untuk melakukan pencarian film berdasarkan judul
'''
def film_search(request):
    
    #TODO ambil data json dari judul film yang dicari
    #contoh query = http://127.0.0.1:8000/search?title=murder%20in%20%20park
    
    title_film = request.GET.get('title').lower()
    title_formatted = '\"{}\"'.format(title_film)
    query = \
    '''
    SELECT * WHERE { 
        ?uri rdf:type snr:Film ;
        snp:id ?id ;
        snp:title ?title ;
        FILTER (
            contains(lcase(str(?title)), %s) 
        )
    }
    ''' % (title_formatted)

    get_film_data(query)

    list_film = [
        {'uri': {'type': 'uri', 'value': 'http://skulite.org/snr/A_Murder_in_the_Park'}, 'id': {'type': 'literal', 'value': '80044562'}, 'title': {'type': 'literal', 'value': 'A Murder in the Park'}},
        {'uri': {'type': 'uri', 'value': 'http://skulite.org/snr/Jailbreak'}, 'id': {'type': 'literal', 'value': '80990658'}, 'title': {'type': 'literal', 'value': 'Jailbreak'}},
        {'uri': {'type': 'uri', 'value': 'http://skulite.org/snr/Cristina'}, 'id': {'type': 'literal', 'value': '80076160'}, 'title': {'type': 'literal', 'value': 'Cristina'}}]

    for film in list_film:
        for key in film:
            film[key] = film[key]['value']

    context = {"list_film" : list_film} 
    return render(request, 'main/list_film.html', context)
