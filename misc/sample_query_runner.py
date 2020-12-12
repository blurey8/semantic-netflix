#!/usr/bin/env python
# coding: utf-8

# # Sample Query Runner
# 
# Dirancang oleh: Tim Skulite  
#   
# Program ini akan berisi contoh penerapan pengambilan data secara lokal menggunakan Apache Jena Fuseki dan remote menggunakan data dari DBPedia / Wikidata

# ## Query dari Server Lokal (Jena Fuseki)
# 
# Jena Fuseki mendukung protokol HTTP untuk mengambil data yang ada didalamnya. Anggaplah Jena Fuseki seperti SQL Server (PostgreSQL, MySQL, lainnya) dan berkas berformat .ttl adalah berkas databasenya (misalnya .sqlite).  
#   
# Pertama harus dijalankan terlebih dahulu Jena Fusekinya. Setelah itu bisa mengambil datanya via HTTP dan kembaliannya adalah sebuah response dengan body-nya adalah datanya. Untuk menjalankan Jena Fuseki bisa menggunakan perintah di terminal *pada directory project*:
# 
# ```
# cd fuseki/
# ./fuseki-server --file=../dataset/movies.ttl /ds
# ```
# 
# Proses ini akan membentuk in-memory instance dan tentunya hanya mendukung operasi READ (belum mencoba operasi lainnya). Setelah menjalankan Jena Fuseki, silakan lanjutkan menjalankan cell dibawah.

# In[1]:


import json
import requests


# In[2]:


# Fungsi untuk menjalankan query
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


# In[3]:


# Contoh query mendapatkan triple S P O dari server lokal
get_response_from_local('SELECT * {?s ?p ?o} LIMIT 5')


# ## Query dari Server Remote (DBpedia / Wikidata)
# 
# Pengambilan data secara remote dapat menggunakan bantuan library bernama RDFLib. Pada contoh kali ini, akan dilakukan pengambilan data Michael Jackson dari Wikidata

# In[4]:


get_ipython().system('pip install rdflib')


# In[5]:


# Import library yang diperlukan
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS
from rdflib.plugins.stores.sparqlstore import SPARQLStore


# In[6]:


# Load Datastore DBPedia dan Wikidata
data_graph_dbpedia = Graph(SPARQLStore("http://dbpedia.org/sparql", context_aware=False))


# In[7]:


# Menjalankan query sederhana
result = data_graph_dbpedia.query('''
SELECT * WHERE {
    ?film rdf:type dbo:Film .
}
LIMIT 5
''')

for row, *_ in result:
    print(row)


# ## Query Secara Gabungan
# 
# Pada bagian ini akan dicoba mengambil data film yang sudah ada di dataset lokal, kemudian menambahkan informasi yang belum ada dari sumber remote yang kemudian hasil akhir pengolahan akan ditampilkan ke pengguna  
#   
# Ada 4 tahap yang akan coba dicover
# 
# 1. Mengambil beberapa film + id nya yang tersedia secara lokal
# 2. Menampilkan sedikit detail dari film dataset lokal berdasarkan ID
# 3. Menampilkan film tertentu secara remote berdasarkan ID dari data lokal
# 4. Menggabungkan hasil query lokal dengan remote

# In[8]:


# Mendefinisikan URI untuk query (INI PENTING)
PREFIXES = '''
PREFIX snr: <http://skulite.org/snr/>
PREFIX snp: <http://skulite.org/snp/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dbr: <http://dbpedia.org/resource/>
'''


# ### 1. Mengambil beberapa film + id nya dari dataset lokal
# Pada bagian ini akan melakukan pengambilan data dari dataset lokal

# In[9]:


query = '''
SELECT *
WHERE { 
    ?individual rdf:type snr:Film ;
    snp:id ?id .
}
LIMIT 5
'''
all_films = get_response_from_local(PREFIXES + query)


# In[10]:


all_films


# ### 2. Menampilkan sedikit detail dari film dataset lokal berdasarkan ID.  
# Pada bagian ini akan melakukan pengambilan beberapa informasi detail dari film  
# Contoh: use case ketika user klik salah satu film dengan ID: 80044562

# In[11]:


query = '''
SELECT * WHERE { 
    ?uri snp:id "80044562" ;
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
'''
local_query_result = get_response_from_local(PREFIXES + query)[0]


# In[12]:


local_query_result


# ### 3. Menampilkan film tertentu secara remote berdasarkan ID dari data lokal
# Pada bagian ini akan melakukan pengambilan data film secara remote berdasarkan ID dari konten tertentu

# In[13]:


# Ambil nama individunya terlebih dahulu (Misal ID: 80044562)

local_query = '''
SELECT *
WHERE { 
    ?individual snp:id "80044562" ;
}
'''
individual = get_response_from_local(PREFIXES + local_query)
movie_name = individual[0]['individual']['value'].split("/")[-1]


# In[14]:


# Mengambil informasi terkait distributor, producer, dan homepage dari film tersebut

remote_query = '''
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
''' % (movie_name, movie_name, movie_name)
remote_query_result = data_graph_dbpedia.query(PREFIXES + remote_query)


# In[15]:


for row in remote_query_result:
    print(row)
    
# Catatan: Jika tidak ada return apapun berarti memang hasil querynya adalah data kosong


# ### 4. Menggabungkan hasil query lokal dengan remote
# Pada bagian ini akan dilakukan penggabungan hasil query dari data lokal dengan hasil query dari data remote dalam bentuk Python dictionary

# In[16]:


movie_details = {}

# Menyimpan hasil query data lokal dalam bentuk dictionary
for key in local_query_result:
    movie_details[key] = local_query_result[key]['value']


# Menyimpan hasil query dalam bentuk dictionary
for row in remote_query_result:
    movie_details['distributor'] = row.distributor
    movie_details['producer'] = row.producer
    movie_details['homepage'] = row.homepage


# In[17]:


movie_details

