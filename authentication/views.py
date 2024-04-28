from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from user.models import Pengguna


# Create your views here.

# Login view
def login_view(request ):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main') 
        else:
            # Invalid login credentials, return to login page with an error message
            print("error")
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        username = request.POST['username']
        password2 = request.POST['password2']
        country = request.POST['country']
        if form.is_valid():
            print(country)
            user = Pengguna(username=username, password=password2, country=country)
            user.save()
            form.save()
            return redirect('authentication:login')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"- {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('main:show_main')

