from django.shortcuts import render
from contributors.models import Contributors, Pemain, PenulisSkenario, Sutradara

def show_contributors(request):
    # Random order
    contributors = Contributors.objects.all()
    return render(request, 'daftar-kontributor.html',{
        'contributors': contributors
    })