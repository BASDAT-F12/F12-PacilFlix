from django.shortcuts import render

# Create your views here.
def list_package(request):
    context = {
        'name': 'PacilFix F12',
        'class': 'BASDAT F'
    }
    return render(request, "daftar-langganan.html", context)

def buy_page(request):
    context = {
        'name': 'PacilFix F12',
        'class': 'BASDAT F'
    }
    return render(request, "halaman-beli.html", context)