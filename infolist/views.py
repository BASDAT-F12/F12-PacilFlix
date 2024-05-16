from django.shortcuts import get_object_or_404,render
from infolist.queries import get_all_movies, get_all_series

def list_tayangan(request):
    movies = get_all_movies()
    series = get_all_series()
    # top10_global = get_top10_tayangan_global()
    # top10_lokal = get_top10_tayangan_lokal('Indonesia')
    return render(request, 'daftar-tayangan.html', {
        'movies': movies,
        'series': series,
    })

    
def search_list(request):
    return render(request, 'search-tayangan.html')

def detail_tayangan_film(request):
    return render(request, 'detail-tayangan-film.html')

def detail_tayangan_series(request):
    return render(request, 'detail-tayangan-series.html')
    
def detail_tayangan_episode(request):
    return render(request, 'detail-tayangan-episode.html')

def show_contributors(request):
    # Random order
    return render(request, 'daftar-kontributor.html',{
        'contributors': ""
    })