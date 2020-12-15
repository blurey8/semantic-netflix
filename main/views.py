from django.shortcuts import render

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








