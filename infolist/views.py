from django.shortcuts import render
from infolist.models import Tayangan, Film, Series, Sutradara

def list_tayangan(request):
    # Random order
    tayangans = Tayangan.objects.order_by('?')[:10]
    films = Film.objects.all()
    series = Series.objects.all()
    return render(request, 'daftar-tayangan.html',{
        'tayangans': tayangans,
        'films': films,
        'series': series
    })