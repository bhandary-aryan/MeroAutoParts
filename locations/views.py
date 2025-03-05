# locations/views.py
from django.shortcuts import render

def petrol_stations(request):
    """View for the petrol stations finder page"""
    return render(request, 'locations/petrol_stations.html')


def nearby_garages(request):
    """View for the nearby garages finder page"""
    return render(request, 'locations/nearby_garages.html')