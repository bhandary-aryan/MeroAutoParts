# locations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('petrol-stations/', views.petrol_stations, name='petrol_stations'),
    path('nearby-garages/', views.nearby_garages, name='nearby_garages'),

    path('save-location/', views.save_location, name='save_location'),
    path('garage/<int:garage_id>/', views.garage_detail, name='garage_detail'),
    path('garage-finder/', views.garage_finder, name='garage_finder'),

]