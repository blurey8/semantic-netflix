from .constants import FUSEKI_URL, PREFIXES

import requests
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS
from rdflib.plugins.stores.sparqlstore import SPARQLStore

data_graph_dbpedia = Graph(SPARQLStore("http://dbpedia.org/sparql", context_aware=False))

#TODO Graph untuk Wikidata belum dibuat untuk saat ini

'''
Fungsi untuk mengambil response data dari dataset lokal
'''
def get_data_from_local(query_to_send):
    try:
        response = requests.post(FUSEKI_URL, data={'query': PREFIXES + query_to_send})
        return response.json()['results']['bindings']
    except ValueError:
        print("JSON Bermasalah atau Jena Fuseki Return 400")
        return []
    except:
        print("Jena Fuseki belum dijalankan")
        return []

'''
Fungsi untuk mengambil response data dari dataset remote
'''
def get_data_from_remote(query_to_send):
    return data_graph_dbpedia.query(PREFIXES + query_to_send)

'''
Fungsi untuk mengambil nama film yang menjadi objek berdasarkan ID
'''
def get_film_object_from_id(film_id):
    id_formatted = '\"{}\"'.format(film_id)
    
    query = \
    '''
    SELECT * WHERE { 
        ?uri snp:id %s ;
    }
    ''' % (id_formatted)
    
    triple = get_data_from_local(query)
    film_object_name = triple[0]['uri']['value'].split("/")[-1]
    
    return film_object_name

'''
Fungsi untuk menggabungkan data dari lokal dan remote
'''
def get_combined_individual_film_detail(query_to_send):
    combined_data = {}
    local_query_result = get_data_from_local(query_to_send)[0]
    print(local_query_result)
    remote_query_result = get_data_from_remote(query_to_send)

    for key in local_query_result:
        combined_data[key] = local_query_result[key]['value']

    for row in remote_query_result:
        combined_data['distributor'] = row.distributor
        combined_data['producer'] = row.producer
        combined_data['homepage'] = row.homepage

    return combined_data
