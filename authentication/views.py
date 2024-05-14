import psycopg2
from psycopg2 import Error as PsycopgError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from authentication.queries import register_user, login_user


# Create your views here.

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if login_user(username, password):
            request.session['is_authenticated'] = True
            request.session['username'] = username
            return redirect('infolist:list-tayangan')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('authentication:login')
    else:
        return render(request, 'login.html')


# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            country = request.POST['country']
            try:
                register_user(username, password, country)
                messages.success(request, 'User registered successfully!')
                return redirect('authentication:login')
            except PsycopgError as e:
                error_message = str(e)
                # Username checking trigger
                if "Username already exists" in error_message:
                    messages.error(request, 'Username already exists. Please choose a different username.')
                else:
                    messages.error(request, f'Error registering user: {error_message}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"- {error}")
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_user(request):
    logout(request)
    request.session['is_authenticated'] = False
    return redirect('main:show_main')

