from django.urls import path
from contributors.views import show_contributors

app_name = 'contributors'

urlpatterns = [
    path('show-contributors/', show_contributors, name='show-contributors'),
]
