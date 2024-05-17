from django.urls import path
from user.views import list_package, buy_page

app_name = 'user'

urlpatterns = [
    path('daftar-langganan/', list_package, name='daftar-langganan'),
    path('halaman-beli/<str:id>/', buy_page, name='halaman-beli')
]