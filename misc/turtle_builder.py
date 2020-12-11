#!/usr/bin/env python
# coding: utf-8

# # Tutle File Builder
# 
# Dirancang oleh: Tim Skulite  
#   
# Program ini dirancang untuk melakukan pembangunan file turtle (TTL) yang berasal dari file CSV. Tidak hanya itu, pada program ini juga akan dilakukan penambahan prefix, individual, class, dan data properties pada berkas TTL yang akan dibaca oleh program yang akan dibangun

# In[1]:


# Melakukan import module

import re
import pandas as pd
import numpy as np
from datetime import datetime


# In[2]:


# Membaca dataset

df = pd.read_csv('movies.csv')
df.head()


# In[3]:


# Menghapus beberapa kolom yang tidak digunakan

df.drop(['duration', 'listed_in'], axis=1, inplace=True)

# Menghapus beberapa baris karena mengandung karakter yang sulit diolah

df = df.drop([528,568,761,762,763,764,765,766,1448,2574,5715])
df.reset_index()


# In[4]:


# Melakukan replacement NaN menjadi string untuk mempermudah pengerjaan

df.columns = ['id', 'category', 'title', 'director',
              'cast', 'country', 'dateAdded',
              'releaseYear', 'rating', 'description']
df = df.replace(np.nan, 'No Data', regex=True)


# In[5]:


# Mengubah pandas dataframe menjadi dictionary

df_to_dict = df.to_dict(orient='records')


# In[6]:


# Konversi string tanggal menjadi format yang didukung RDF

def convert_month_to_num(raw_date):  
    dates = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }
    raw_date = raw_date.replace(",", "")
    splitted_date = raw_date.split(" ")
    
    if len(splitted_date) == 4:
        splitted_date.pop(0)
    
    month = splitted_date[0]
    date = splitted_date[1]
    year = splitted_date[2]

    month = dates[month]

    if int(date) < 10:
        date = "0" + str(date)
    if int(month) < 10:
        month = "0" + str(month)
    
    return "{}-{}-{}".format(year, month, date)


# In[7]:


# Prefixes

prefixes = '''
############################
#    Prefixes
############################

PREFIX snr: <http://skulite.org/snr/>
PREFIX snp: <http://skulite.org/snp/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
'''

# Class Properties

class_properties = '''
############################
#    Classes
############################

snr:Content rdf:type owl:Class .
snr:Series rdf:type owl:Class ; rdfs:subClassOf snr:Content .
snr:Film rdf:type owl:Class ; rdfs:subClassOf snr:Content .
'''

# Data Properties

data_properties = '''
############################
#    Data properties
############################

snp:title rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:id rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:description rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:releaseYear rdfs:domain snr:Content ; rdfs:range xsd:gYear .
snp:category rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:rating rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:director rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:cast rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:country rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:dateAdded rdfs:domain snr:Content ; rdfs:range xsd:date .
snp:numberOfSeasons rdfs:domain snr:Series ; rdfs:range xsd:integer .
snp:duration rdfs:domain snr:Film ; rdfs:range xsd:duration . 
'''

# Individuals

individuals = '''
############################
#    Individuals
############################

'''


# In[8]:


# Pengolahan CSV menjadi berkas TTL yang didukung 

columns = ['title', 'id', 'description', 'releaseYear',
           'category', 'rating', 'director',
           'cast', 'country', 'dateAdded']

def convert_id(string):
    return '\"{}\"'.format(string)

def convert_title_for_object(string):
    string = re.sub(r'[^\w\s]','', string)
    return string.replace("\n", " ").replace(" ", "_").replace("  ", "_")

def convert_universal(string):
    string = string.replace("\"", "").replace("\'", "").replace("\n", " ")
    return '\"{}\"'.format(string)

def convert_release(string):
    return '\"{}\"'.format(string)
    
def convert_category_rating(string):
    string = string.replace(" ", "-")
    return '\"{}\"'.format(string)
    
def convert_date_added(string):
    return '\"{}\"'.format(convert_month_to_num(string))
    
def start_process():
    global individuals
    
    for i in range (len(df_to_dict)):

        data = ""
        for j in range (len(columns)):
            current_column = columns[j]
            column_value = df_to_dict[i][current_column]

            if column_value != 'No Data':
                                
                if current_column == 'title':
                    data += "snr:{} ".format(convert_title_for_object(column_value))
                    data += "rdf:type snr:Content ; "
                    column_value = convert_universal(column_value)
                
                if current_column == 'id':
                    column_value = convert_id(column_value)
                
                if current_column == 'releaseYear':
                    column_value = convert_release(column_value)
                
                if current_column == 'description' or current_column == 'director' or current_column == 'cast' or current_column == 'country':
                    column_value = convert_universal(column_value)
                    
                if current_column == 'category' or current_column == 'rating':
                    column_value = convert_category_rating(column_value)
                
                if current_column == 'dateAdded':
                    column_value = convert_date_added(column_value)
        
                data += 'snp:{} {}'.format(current_column, column_value)

                if j != len(columns) - 1:
                    data += ' ; '
                else:
                    data += ' .'

            else:
                if current_column == 'dateAdded':
                    data = data[:-3]
                    data += ' .'

        individuals += data + '\n'


# In[9]:


# Memulai pemrosesan data

start_process()


# In[10]:


# Compile menjadi file TTL

final_data = prefixes + class_properties + data_properties + individuals
file = open('movies.ttl', 'w')
file.write(final_data)
file.close()

