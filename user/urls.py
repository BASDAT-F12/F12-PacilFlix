from django.urls import path
from user.views import list_package

app_name = 'user'

urlpatterns = [
    path('daftar-langganan/', list_package, name='daftar-langganan'),
]