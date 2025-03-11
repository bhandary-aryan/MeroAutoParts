# locations/management/commands/populate_garage_data.py
from django.core.management.base import BaseCommand
from locations.models import Garage, GarageExpertise
from core.models import Category
import random

class Command(BaseCommand):
    help = 'Adds specialization data to existing garages'
    
    def handle(self, *args, **options):
        # Get all garages and categories
        garages = Garage.objects.all()
        categories = Category.objects.all()
        
        if not garages:
            self.stdout.write(self.style.ERROR('No garages found. Please create garages first.'))
            return
            
        if not categories:
            self.stdout.write(self.style.ERROR('No part categories found. Please create categories first.'))
            return
        
        # Add random specializations
        for garage in garages:
            # Choose 3-6 random categories
            num_categories = random.randint(3, 6)
            selected_categories = random.sample(list(categories), min(num_categories, len(categories)))
            
            # Add specializations
            for category in selected_categories:
                garage.specializations.add(category)
                
                # Add expertise level
                expertise_level = random.randint(1, 4)
                GarageExpertise.objects.create(
                    garage=garage,
                    part_category=category,
                    expertise_level=expertise_level
                )
            
            # Add random rating
            garage.average_rating = round(random.uniform(3.0, 5.0), 1)
            garage.total_reviews = random.randint(5, 50)
            garage.save()
            
            self.stdout.write(self.style.SUCCESS(f'Added specializations to {garage.name}'))