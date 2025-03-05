# locations/models.py
from django.db import models

class PetrolStation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name