from django.urls import path
from infolist.views import list_tayangan

app_name = 'infolist'

urlpatterns = [
    path('list-tayangan/', list_tayangan, name='list-tayangan'),
]
