from django.shortcuts import render

def show_contributors(request):
    # Random order
    return render(request, 'daftar-kontributor.html',{
        'contributors': ""
    })