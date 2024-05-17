from django.shortcuts import get_object_or_404,render,redirect
from django.http import JsonResponse
import psycopg2
from psycopg2 import IntegrityError
from infolist.queries import get_all_movies, get_all_series, get_search_result, get_movie_data, \
                            get_all_contributors, get_series_data, get_episode_data, get_top10_tayangan_global,\
                            get_reviews, insert_review


def list_tayangan(request):
    movies = get_all_movies()
    series = get_all_series()
    top10_global = get_top10_tayangan_global()
    # top10_lokal = get_top10_tayangan_lokal('Indonesia')
    return render(request, 'daftar-tayangan.html', {
        'top10_global': top10_global,
        'movies': movies,
        'series': series,
    })

def search_list(request):
    query = request.GET.get('q', '')
    if query:
        results = get_search_result(query)
    else:
        results = []
    return render(request, 'search-tayangan.html', {
        'results': results,
    })

def detail_tayangan_film(request, id):
    movie_data = get_movie_data(id)
    reviews = get_reviews(id)
    error_message = None

    if request.method == 'POST':
        username = request.session.get('username')

        rating = int(request.POST['rating']) 
        review = request.POST['review_text']  

        message = insert_review(id, username, rating, review)
        if message != "Review berhasil ditambahkan.":
            error_message = message
        else:
            return redirect('infolist:detail_tayangan_film', id=id)

    return render(request, 'detail-tayangan-film.html', {
        'movie_data': movie_data,
        'reviews': reviews,
        'error_message': error_message,
    })

def detail_tayangan_series(request,id):
    series_data = get_series_data(id)
    reviews = get_reviews(id)
    error_message = None
    if request.method == 'POST':
        username = request.session.get('username')
        rating = int(request.POST['rating'])
        review = request.POST['review_text']
        message = insert_review(id, username, rating, review)
        if message != "Review berhasil ditambahkan.":
            error_message = message
        else:
            return redirect('infolist:detail_tayangan_series', id=id)
    return render(request, 'detail-tayangan-series.html',{
        'series_data': series_data,
        'reviews': reviews,
        'error_message': error_message
    })
    
def detail_tayangan_episode(request,id,name):
    episode_data = get_episode_data(id,name)
    
    return render(request, 'detail-tayangan-episode.html', {
        'episode_data': episode_data
    })

def show_contributors(request):
    contributors = get_all_contributors()
    return render(request, 'daftar-kontributor.html',{
        'contributors': contributors
    })


