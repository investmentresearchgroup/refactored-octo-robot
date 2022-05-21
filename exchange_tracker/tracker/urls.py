from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tracker-index'),
    path('contactus/', views.contact_us, name='contactus'),
    path('single/<int:pk>/', views.single, name='tracker-single'),
    path('search/', views.single_search, name='tracker-search'),
]
