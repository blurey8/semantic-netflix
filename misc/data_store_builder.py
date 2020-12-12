#!/usr/bin/env python
# coding: utf-8

# # Data Store Builder
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

df.drop(['type'], axis=1, inplace=True)

# Menghapus beberapa baris karena mengandung karakter yang sulit diolah

df = df.drop([528,568,761,762,763,764,765,766,1448,2574,5715])
df.reset_index()
df.head()


# In[4]:


# Melakukan replacement NaN menjadi string untuk mempermudah pengerjaan

df.columns = ['id', 'title', 'director',
              'cast', 'country', 'dateAdded',
              'releaseYear', 'rating', 'playtime',
              'category', 'description']
df = df.replace(np.nan, 'No Data', regex=True)
df.head()


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

snp:id rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:title rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:director rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:cast rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:country rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:dateAdded rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:releaseYear rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:rating rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:numOfSeasons rdfs:domain snr:Series ; rdfs:range xsd:string .
snp:duration rdfs:domain snr:Film ; rdfs:range xsd:string . 
snp:category rdfs:domain snr:Content ; rdfs:range xsd:string .
snp:description rdfs:domain snr:Content ; rdfs:range xsd:string .
'''

# Individuals

individuals = '''
############################
#    Individuals
############################

'''


# In[8]:


# Fungsi untuk mengolah data mentah

def convert_id(string):
    return '\"{}\"'.format(string)

def convert_title_for_object(string):
    string = re.sub(r'[^\w\s]','', string)
    return string.replace("\n", " ").replace(" ", "_").replace("  ", "_")

def convert_universal(string):
    string = string.replace("\"", "").replace("\'", "").replace("\n", " ")
    return '\"{}\"'.format(string)

def convert_date_added(string):
    return '\"{}\"'.format(convert_month_to_num(string))

def convert_release(string):
    return '\"{}\"'.format(string)
    
def convert_category_rating(string):
    string = string.replace("\"", "").replace("\'", "")
    return '\"{}\"'.format(string)
    
def convert_playtime(string):
    duration_pattern = "^.*min"
    season_pattern = "^.*(Seasons|Season)"

    time_value = '\"{}\"'.format(string)
    
    if re.match(duration_pattern,string):
        return [time_value, "film"]
    elif re.match(season_pattern,string):
        return [time_value, "series"]


# In[9]:


# Pengolahan CSV menjadi berkas TTL yang didukung 

columns = ['title', 'id', 'director',
           'cast', 'country', 'dateAdded',
           'releaseYear', 'rating', 'playtime',
           'category', 'description']

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
                    column_value = convert_universal(column_value)
                
                if current_column == 'id':
                    column_value = convert_id(column_value)
                
                if current_column == 'director' or current_column == 'cast' or current_column == 'country' or current_column == 'description':
                    column_value = convert_universal(column_value)

                if current_column == 'dateAdded':
                    column_value = convert_date_added(column_value)                    
                    
                if current_column == 'releaseYear':
                    column_value = convert_release(column_value)
                
                if current_column == 'rating' or current_column == 'category':
                    column_value = convert_category_rating(column_value)

                if current_column != 'playtime':
                    data += 'snp:{} {}'.format(current_column, column_value)
                    
                if current_column == 'playtime':
                    converted_playtime = convert_playtime(column_value)
                    
                    if converted_playtime[1] == 'film':
                        data += 'rdf:type snr:Film ; '
                        data += 'snp:duration {}'.format(converted_playtime[0])
                    else:
                        data += 'rdf:type snr:Series ; '
                        data += 'snp:numOfSeasons {}'.format(converted_playtime[0])

                if j != len(columns) - 1:
                    data += ' ; '
                else:
                    data += ' .'

            else:
                if current_column == 'description':
                    data = data[:-3]
                    data += ' .'

        individuals += data + '\n'


# In[10]:


# Memulai pemrosesan data

start_process()


# In[11]:


# Compile menjadi file TTL

final_data = prefixes + class_properties + data_properties + individuals
file = open('movies.ttl', 'w')
file.write(final_data)
file.close()

