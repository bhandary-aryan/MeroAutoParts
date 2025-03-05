# locations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('petrol-stations/', views.petrol_stations, name='petrol_stations'),
    path('nearby-garages/', views.nearby_garages, name='nearby_garages'),

]