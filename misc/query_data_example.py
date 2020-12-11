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
# Pertama harus dijalankan terlebih dahulu Jena Fusekinya. Setelah itu bisa mengambil datanya via HTTP dan kembaliannya adalah sebuah response dengan body-nya adalah datanya. Untuk menjalankan Jena Fuseki bisa menggunakan perintah di terminal:
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


# In[6]:


# Melakukan import terhadap suatu berkas entity yang akan menjadi graf
g = Graph()
g.parse('https://www.wikidata.org/wiki/Special:EntityData/Q2831.ttl')


# In[7]:


# Banyaknya elemen
len(g)


# In[8]:


# Menjalankan query sederhana
qres = g.query('''
SELECT ?label
WHERE {
wd:Q2831 skos:altLabel ?label .
}
LIMIT 5
''')

for label, *_ in qres:
    print(label.value, "<->", label.language)


# ## Query Secara Gabungan
# 
# Pada bagian ini akan dicoba mengambil data film yang sudah ada di dataset lokal, kemudian menambahkan informasi yang belum ada dari sumber remote yang kemudian hasil akhir pengolahan akan ditampilkan ke pengguna  
#   
# Ada 4 tahap yang akan coba dicover
# 
# 1. Mengambil beberapa film + id nya yang tersedia secara lokal
# 2. Menampilkan sedikit detail dari film dataset lokal berdasarkan ID
# 3. Menampilkan film tertentu secara remote berdasarkan ID dari data lokal
# 4. Mengambil informasi yang  kurang dari film tersebut secara remote
# 5. Menampilkan kepada pengguna

# In[9]:


# Mendefinisikan URI untuk query (INI PENTING)
PREFIXES = '''
PREFIX snr: <http://skulite.org/snr/>
PREFIX snp: <http://skulite.org/snp/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''


# In[10]:


# 1. Mengambil beberapa film + id nya dari dataset lokal

query = '''
SELECT *
WHERE { 
    ?individual rdf:type snr:Content .
    ?individual snp:id ?id
}
LIMIT 5
'''

get_response_from_local(PREFIXES + query)


# In[11]:


# 2. Menampilkan sedikit detail dari film dataset lokal berdasarkan ID. Contoh: use case ketika user klik salah satu film dengan ID: 70136114

query = '''
SELECT ?title ?description ?releaseYear ?category
WHERE { 
    ?individual snp:id "70136114" ;
    snp:title ?title ;
    snp:description ?description ;
    snp:releaseYear ?releaseYear ;
    snp:category ?category .
}
'''

get_response_from_local(PREFIXES + query)


# In[12]:


# 3. Menampilkan film tertentu secara remote berdasarkan ID dari data lokal
# SEGERA HADIR


# In[13]:


# 4. Mengambil informasi yang  kurang dari film tersebut secara remote
# SEGERA HADIR


# In[14]:


# 5. Menampilkan kepada pengguna
# SEGERA HADIR

