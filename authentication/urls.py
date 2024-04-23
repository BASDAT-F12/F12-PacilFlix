from django.urls import path
from authentication.views import login_view, register

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
]