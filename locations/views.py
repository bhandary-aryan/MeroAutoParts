# locations/views.py
from django.shortcuts import render

def petrol_stations(request):
    """View for the petrol stations finder page"""
    return render(request, 'locations/petrol_stations.html')


def nearby_garages(request):
    """View for the nearby garages finder page"""
    return render(request, 'locations/nearby_garages.html')

# locations/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request.session['user_lat'] = float(data.get('lat'))
            request.session['user_lon'] = float(data.get('lon'))
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# locations/views.py (additional function)
from django.shortcuts import render, get_object_or_404
from .models import Garage
from .utils import haversine

def garage_detail(request, garage_id):
    garage = get_object_or_404(Garage, id=garage_id)
    
    # Get user location
    user_lat = request.session.get('user_lat', 27.7172)
    user_lon = request.session.get('user_lon', 85.3240)
    
    # Calculate distance
    distance = haversine(
        garage.longitude, 
        garage.latitude, 
        user_lon, 
        user_lat
    )
    
    # Get expertise areas
    expertise_areas = garage.expertise_areas.all().select_related('part_category')
    
    # Get reviews
    reviews = garage.reviews.all().select_related('user')[:10]
    
    context = {
        'garage': garage,
        'distance': distance,
        'expertise_areas': expertise_areas,
        'reviews': reviews
    }
    
    return render(request, 'locations/garage_detail.html', context)

def garage_finder(request):
    # Get all garages
    garages = Garage.objects.all()
    
    # Get filter parameters
    part_id = request.GET.get('part_id')
    
    # Apply filters
    if part_id:
        from core.models import Product
        product = get_object_or_404(Product, id=part_id)
        part_category_id = product.category.id
        garages = garages.filter(specializations__id=part_category_id)
    
    # Get user location
    user_lat = request.session.get('user_lat', 27.7172)
    user_lon = request.session.get('user_lon', 85.3240)
    
    # Calculate distances and sort
    garage_list = []
    for garage in garages:
        distance = haversine(
            garage.longitude, 
            garage.latitude, 
            user_lon, 
            user_lat
        )
        garage_list.append({
            'garage': garage,
            'distance': distance
        })
    
    # Sort by distance
    sorted_garages = sorted(garage_list, key=lambda x: x['distance'])
    
    context = {
        'garages': sorted_garages,
        'part_id': part_id
    }
    
    return render(request, 'locations/nearby_garages.html', context)
