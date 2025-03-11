# locations/models.py
from django.db import models
from django.contrib.auth.models import User
from core.models import Category as PartCategory
from django.conf import settings  

class PetrolStation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name
    

class Garage(models.Model):
    # Existing fields
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(blank=True)
    
    # New fields for part recommendations
    specializations = models.ManyToManyField(PartCategory, related_name='specialized_garages')
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_reviews = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    operating_hours = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return self.name

class GarageReview(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('garage', 'user')
        
    def __str__(self):
        return f"{self.user.username}'s review for {self.garage.name}"

class GarageExpertise(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE, related_name='expertise_areas')
    part_category = models.ForeignKey(PartCategory, on_delete=models.CASCADE)
    expertise_level = models.IntegerField(choices=[
        (1, 'Basic'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
        (4, 'Specialist')
    ])
    
    class Meta:
        unique_together = ('garage', 'part_category')
        
    def __str__(self):
        return f"{self.garage.name} - {self.part_category.name} ({self.get_expertise_level_display()})"
