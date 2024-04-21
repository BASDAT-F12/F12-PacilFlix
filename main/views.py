from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'PacilFix F12',
        'class': 'BASDAT F'
    }

    return render(request, "main.html", context)