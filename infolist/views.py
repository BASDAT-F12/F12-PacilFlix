from django.shortcuts import get_object_or_404,render
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
    
def detail_tayangan(request, tayangan_id):
    tayangan = get_object_or_404(Tayangan, pk=tayangan_id)
    if isinstance(tayangan, Film):
        tayangan_type = 'film'
    elif isinstance(tayangan, Series):
        tayangan_type = 'series'
    else:
        return None
    return render(request, 'detail-tayangan.html',{
        'tayangan': tayangan,
        'tayangan_type': tayangan_type
        })