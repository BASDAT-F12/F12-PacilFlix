from django.urls import path

from infolist.views import list_tayangan, detail_tayangan_episode,detail_tayangan_film,detail_tayangan_series, search_list, show_contributors

app_name = 'infolist'

urlpatterns = [
    path('list-tayangan/', list_tayangan, name='list-tayangan'),
    path('search-tayangan/', search_list, name='search_list'),
    path('detail-tayangan-film/<str:id>/', detail_tayangan_film, name='detail_tayangan_film'),
    path('detail-tayangan-series/', detail_tayangan_series, name='detail_tayangan_series'),
    path('detail-tayangan-episode/', detail_tayangan_episode, name='detail_tayangan_episode'),
    path('show-contributors/', show_contributors, name='show-contributors'),
]
