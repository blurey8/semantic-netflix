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
        return None
    except:
        print("Jena Fuseki belum dijalankan")
        return None

'''
Fungsi untuk mengambil response data dari dataset remote
'''
def get_data_from_remote(query_to_send):
    return data_graph_dbpedia.query(PREFIXES + query_to_send)

'''
Fungsi untuk menggabungkan data dari lokal dan remote
'''
def get_film_data(query_to_send):
    combined_data = {}
    local_query_result = get_data_from_local(query_to_send)
    remote_query_result = get_data_from_remote(query_to_send)

    if local_data != None:
        for key in local_query_result:
            combined_data[key] = local_query_result[key]['value']

        for row in remote_query_result:
            combined_data['distributor'] = row.distributor
            combined_data['producer'] = row.producer
            combined_data['homepage'] = row.homepage    
    else:
        print("Query data tidak dapat dilakukan")
    return combined_data
