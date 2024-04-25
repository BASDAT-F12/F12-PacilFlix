from django.urls import path
from authentication.views import login_view, register, logout_view

app_name = 'authentication'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout')
]