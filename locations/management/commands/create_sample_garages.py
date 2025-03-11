# locations/management/commands/create_sample_garages.py
from django.core.management.base import BaseCommand
from locations.models import Garage
import random

class Command(BaseCommand):
    help = 'Create sample garages for testing'

    def handle(self, *args, **options):
        # Sample data for garages in Kathmandu
        sample_garages = [
            {
                'name': 'Auto Tech Garage',
                'address': 'Kalanki, Kathmandu',
                'phone_number': '01-4671234',
                'email': 'autotech@example.com',
                'latitude': 27.6944,
                'longitude': 85.2797,
                'description': 'Full-service auto repair and maintenance garage specializing in Japanese vehicles.',
                'operating_hours': 'Mon-Sat: 8 AM - 6 PM'
            },
            {
                'name': 'Nepal Motors Workshop',
                'address': 'Balaju, Kathmandu',
                'phone_number': '01-4356789',
                'email': 'nepalmotors@example.com',
                'latitude': 27.7352,
                'longitude': 85.3018,
                'description': 'Authorized service center for multiple brands with state-of-the-art diagnostic equipment.',
                'operating_hours': 'Mon-Fri: 9 AM - 5 PM, Sat: 9 AM - 2 PM'
            },
            {
                'name': 'Kathmandu Auto Care',
                'address': 'New Baneshwor, Kathmandu',
                'phone_number': '01-4567890',
                'email': 'ktmlautocare@example.com',
                'latitude': 27.6911,
                'longitude': 85.3434,
                'description': 'Specialized in electrical systems and engine performance optimization.',
                'operating_hours': 'Mon-Sat: 7 AM - 7 PM'
            },
            {
                'name': 'Himalayan Auto Repairs',
                'address': 'Chabahil, Kathmandu',
                'phone_number': '01-4432109',
                'email': 'himalayanauto@example.com',
                'latitude': 27.7208,
                'longitude': 85.3530,
                'description': 'Family-owned garage with 25 years of experience in all types of vehicle repairs.',
                'operating_hours': 'Daily: 8 AM - 8 PM'
            },
            {
                'name': 'Everest Motors',
                'address': 'Naxal, Kathmandu',
                'phone_number': '01-4123456',
                'email': 'everestmotors@example.com',
                'latitude': 27.7172,
                'longitude': 85.3365,
                'description': 'Premium service center specializing in European luxury vehicles.',
                'operating_hours': 'Mon-Fri: 9 AM - 6 PM'
            },
            {
                'name': 'Valley Auto Workshop',
                'address': 'Patan, Lalitpur',
                'phone_number': '01-5534567',
                'email': 'valleyauto@example.com',
                'latitude': 27.6710,
                'longitude': 85.3177,
                'description': 'Comprehensive repair services with transparent pricing and free estimates.',
                'operating_hours': 'Mon-Sat: 8:30 AM - 5:30 PM'
            },
            {
                'name': 'Bhaktapur Auto Clinic',
                'address': 'Suryabinayak, Bhaktapur',
                'phone_number': '01-6612345',
                'email': 'bhaktapurauto@example.com',
                'latitude': 27.6725,
                'longitude': 85.4009,
                'description': 'Traditional expertise combined with modern technology for reliable repairs.',
                'operating_hours': 'Mon-Sat: 9 AM - 5 PM'
            }
        ]
        
        # Create garages
        garages_created = 0
        for garage_data in sample_garages:
            # Check if garage with this name already exists
            if not Garage.objects.filter(name=garage_data['name']).exists():
                Garage.objects.create(**garage_data)
                garages_created += 1
                self.stdout.write(self.style.SUCCESS(f"Created garage: {garage_data['name']}"))
            else:
                self.stdout.write(self.style.WARNING(f"Garage already exists: {garage_data['name']}"))
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {garages_created} sample garages"))