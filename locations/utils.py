# locations/utils.py
from math import radians, cos, sin, asin, sqrt
from .models import Garage, GarageExpertise

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r

def get_recommended_garages(part_category_id, user_lat, user_lon, limit=5):
    """
    Returns recommended garages for a specific part category based on:
    1. Expertise with the part
    2. Proximity to user
    3. Garage rating
    """
    # Get all garages with expertise in this part category
    garages_with_expertise = GarageExpertise.objects.filter(
        part_category_id=part_category_id
    ).select_related('garage')
    
    # Calculate scores and distances
    garage_scores = []
    for expertise in garages_with_expertise:
        garage = expertise.garage
        
        # Calculate distance
        distance = haversine(garage.longitude, garage.latitude, user_lon, user_lat)
        
        # Calculate combined score (lower is better)
        # Expertise level is 1-4, we want higher expertise to have lower score
        expertise_score = 5 - expertise.expertise_level
        
        # Rating is 0-5, we want higher rating to have lower score
        rating_score = 5 - float(garage.average_rating or 0)
        
        # Distance in km, closer is better
        distance_score = distance
        
        # Combined score (weighted) - lower is better
        combined_score = (expertise_score * 0.5) + (rating_score * 0.3) + (distance_score * 0.2)
        
        garage_scores.append({
            'garage': garage,
            'distance': distance,
            'expertise_level': expertise.expertise_level,
            'score': combined_score
        })
    
    # Sort by score (lower is better)
    sorted_garages = sorted(garage_scores, key=lambda x: x['score'])
    
    # Return the top results
    return sorted_garages[:limit]