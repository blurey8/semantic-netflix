import requests
from .constants import *


'''
Fungsi untuk mengambil response data dari dataset lokal
'''
def get_data(query_to_send, destination=FUSEKI_URL):
    try:
        response = requests.get(destination, params = {
            'format': 'json',
            'query': PREFIXES + query_to_send
            }
        )
        return response.json()['results']['bindings']
    except ValueError:
        print("JSON Bermasalah atau Hasil Query Return 400")
        return []
    except:
        print("Terjadi Kesalahan")
        return []

'''
Fungsi untuk mengambil semua film
'''
def get_all_films():
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

    query_result = get_data(query)
    return query_result

'''
Fungsi untuk mengambil nama film yang menjadi objek berdasarkan ID dari dataset lokal
'''
def get_film_object_dbpedia(film_id):
    id_formatted = '\"{}\"'.format(film_id)
    
    query = \
    '''
    SELECT * WHERE {?uri snp:id %s.}
    ''' % (id_formatted)
    
    triple = get_data(query)

    if len(triple) > 0:
        film_object_name = triple[0]['uri']['value'].split("/")[-1]
        return film_object_name
    return None

'''
Fungsi untuk mengambil nama film yang menjadi objek berdasarkan ID dari dataset Wikidata
'''
def get_film_object_wikidata(film_id):
    id_formatted = '\"{}\"'.format(film_id)

    query = \
    '''
    SELECT ?title WHERE {
        ?uri snp:id %s.
        ?uri snp:title ?title.
    }
    ''' % (id_formatted)
    
    triple = get_data(query)
    film_title = triple[0]['title']['value']
    title_formatted = '\"{}\"'.format(film_title)

    query = \
    '''
    SELECT DISTINCT ?uri WHERE {
        VALUES ?type {wd:Q5398426 wd:Q11424} ?uri wdt:P31 ?type.
        ?uri rdfs:label ?queryByTitle.
        OPTIONAL {?uri wdt:P1476 ?name.}
        FILTER(REGEX(?queryByTitle, %s, "i"))
    }
    LIMIT 1
    ''' % (title_formatted)

    triple = get_data(query, WIKIDATA_URL)

    if len(triple) > 0:
        film_object_name = triple[0]['uri']['value'].split("/")[-1]
        return film_object_name
    return None

'''
Fungsi untuk mengambil detail sebuah film  dari lokal
'''
def get_film_detail_local(film_id):
    id_formatted = '\"{}\"'.format(film_id)

    query = \
    '''
    SELECT * WHERE { 
        ?uri snp:id %s;
        snp:title ?title;
        snp:director ?director;
        snp:country ?country;
        snp:dateAdded ?dateAdded;
        snp:releaseYear ?releaseYear;
        snp:rating ?rating;
        snp:category ?category;
        snp:description ?description;
        OPTIONAL {?uri snp:duration ?duration.}
        OPTIONAL {?uri snp:numOfSeasons ?season.}
    }
    ''' % (id_formatted)

    query_result = get_data(query)

    if len(query_result) > 0:
        return film_detail_formatter(query_result[0])
    return {}

'''
Fungsi untuk mengambil detail sebuah film  dari DBPedia
'''
def get_film_detail_dbpedia(film_object_name):
    query = \
    '''
    SELECT * WHERE {
        OPTIONAL {dbr:%s dbo:distributor ?distributor.}
        OPTIONAL {dbr:%s dbo:producer ?producer.}
        OPTIONAL {dbr:%s foaf:homepage ?homepage.}
    }
    ''' % (film_object_name, film_object_name, film_object_name)

    query_result = get_data(query, DBPEDIA_URL)

    if len(query_result) > 0:
        return film_detail_formatter(query_result[0])
    return {}

'''
Fungsi untuk mengambil detail sebuah film  dari DBPedia
'''
def get_film_detail_wikidata(film_object_name):
    query = \
    '''
    SELECT * WHERE {
        OPTIONAL {wd:%s wdt:P750 ?distributor.}
        OPTIONAL {wd:%s wdt:P170 ?producer.}
        OPTIONAL {wd:%s wdt:P856 ?homepage.}
        OPTIONAL {wd:%s wdt:P18 ?image.}
    }
    ''' % (film_object_name, film_object_name, film_object_name, film_object_name)

    query_result = get_data(query, WIKIDATA_URL)
    
    if len(query_result) > 0:
        return film_detail_formatter(query_result[0])
    return {}

'''
Film detail formatter untuk dictionary hasil query dengan susunan yang lebih nyaman dibaca
'''
def film_detail_formatter(query_result):
    for key in query_result:
        query_result[key] = query_result[key]['value']
    return query_result
