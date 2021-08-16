from django.urls import path
from .views import display_data

app_name = 'Ticker'

urlpatterns = [
    path('',display_data,name='main-ticker-view')
]
