from django.shortcuts import get_object_or_404,render

def list_tayangan(request):
    # Random order
    return render(request, 'daftar-tayangan.html')
    
def search_list(request):
    return render(request, 'search-tayangan.html')

def detail_tayangan_film(request):
    return render(request, 'detail-tayangan-film.html')

def detail_tayangan_series(request):
    return render(request, 'detail-tayangan-series.html')
    
def detail_tayangan_episode(request):
    return render(request, 'detail-tayangan-episode.html')