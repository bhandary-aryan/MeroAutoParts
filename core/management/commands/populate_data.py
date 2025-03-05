# core/management/commands/populate_data.py
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from core.models import Category, Product

class Command(BaseCommand):
    help = 'Populate database with sample data'
    
    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {'name': 'Bike Parts', 'description': 'Parts for motorcycles and bicycles'},
            {'name': 'Car Parts', 'description': 'Parts for cars and sedans'},
            {'name': 'Jeep Parts', 'description': 'Parts for jeeps and off-road vehicles'},
            {'name': 'Bus Parts', 'description': 'Parts for buses and commercial vehicles'},
            {'name': 'Truck Parts', 'description': 'Parts for trucks and heavy-duty vehicles'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
        
        # Sample product data per category
        product_data = {
            'Bike Parts': [
                {'name': 'Motorcycle Chain', 'brand': 'DID', 'model_no': 'MC-525ZVM-X'},
                {'name': 'Bike Brake Pads', 'brand': 'Brembo', 'model_no': 'BP-07082'},
                {'name': 'Motorcycle Air Filter', 'brand': 'K&N', 'model_no': 'HA-1008'},
                {'name': 'Bike Clutch Plate', 'brand': 'EBC', 'model_no': 'CK1312'},
                {'name': 'Bike Oil Filter', 'brand': 'Bosch', 'model_no': 'OF-3300'},
            ],
            'Car Parts': [
                {'name': 'Car Battery', 'brand': 'Exide', 'model_no': 'CB-75D23L'},
                {'name': 'Car Alternator', 'brand': 'Denso', 'model_no': 'ALT-102211'},
                {'name': 'Car Brake Disc', 'brand': 'Ferodo', 'model_no': 'DDF1557'},
                {'name': 'Car Headlight Bulb', 'brand': 'Philips', 'model_no': 'H7-12V'},
                {'name': 'Car Wiper Blade', 'brand': 'Bosch', 'model_no': 'WB-26'},
            ],
            'Jeep Parts': [
                {'name': 'Jeep Suspension Kit', 'brand': 'Rough Country', 'model_no': 'RC-6715'},
                {'name': 'Jeep Bumper', 'brand': 'Smittybilt', 'model_no': 'SB-76806'},
                {'name': 'Jeep Winch', 'brand': 'Warn', 'model_no': 'W-8274'},
                {'name': 'Jeep LED Light Bar', 'brand': 'Rigid', 'model_no': 'RG-130314'},
                {'name': 'Jeep Fender Flares', 'brand': 'Bushwacker', 'model_no': 'BW-10926-07'},
            ],
            'Bus Parts': [
                {'name': 'Bus Brake System', 'brand': 'Meritor', 'model_no': 'MB-54321'},
                {'name': 'Bus Door Mechanism', 'brand': 'Vapor', 'model_no': 'VD-2300'},
                {'name': 'Bus Air Compressor', 'brand': 'Bendix', 'model_no': 'BA-9090'},
                {'name': 'Bus Mirror', 'brand': 'Hadley', 'model_no': 'HM-H1400'},
                {'name': 'Bus Seat', 'brand': 'Recaro', 'model_no': 'RS-9100'},
            ],
            'Truck Parts': [
                {'name': 'Truck Engine Piston', 'brand': 'Mahle', 'model_no': 'MP-3530'},
                {'name': 'Truck Air Filter', 'brand': 'Fleetguard', 'model_no': 'FA-4557'},
                {'name': 'Truck Radiator', 'brand': 'Modine', 'model_no': 'MR-1234'},
                {'name': 'Truck Brake Drum', 'brand': 'Gunite', 'model_no': 'GBD-3600'},
                {'name': 'Truck Starter', 'brand': 'Delco Remy', 'model_no': 'DS-8200'},
            ],
        }
        
        # Add products for each category
        categories = Category.objects.all()
        
        for category in categories:
            # Get the appropriate products for this category
            parts_data = product_data.get(category.name, [])
            
            for part in parts_data:
                # Create a unique slug that includes the category to avoid conflicts
                slug = slugify(f"{part['name']}-{part['brand']}-{category.name}")
                
                # Check if product already exists
                if not Product.objects.filter(slug=slug).exists():
                    product = Product.objects.create(
                        name=part['name'],
                        category=category,
                        slug=slug,
                        brand=part['brand'],
                        model_no=part['model_no'],
                        description=f"This is a high-quality {part['name']} manufactured by {part['brand']}. It's compatible with most {category.name.lower()}.",
                        price=random.randint(500, 10000),  # Random price between 500-10000
                        stock=random.randint(5, 50),  # Random stock between 5-50
                        # Note: We'll need to handle the image separately
                    )
                    self.stdout.write(self.style.SUCCESS(f'Created product: {product.name} in {category.name}'))
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))