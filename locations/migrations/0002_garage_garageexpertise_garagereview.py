# Generated by Django 5.1.6 on 2025-03-11 08:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_user_email_verified_user_verification_token'),
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Garage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('description', models.TextField(blank=True)),
                ('average_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_reviews', models.IntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('operating_hours', models.CharField(blank=True, max_length=255)),
                ('specializations', models.ManyToManyField(related_name='specialized_garages', to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='GarageExpertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise_level', models.IntegerField(choices=[(1, 'Basic'), (2, 'Intermediate'), (3, 'Advanced'), (4, 'Specialist')])),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expertise_areas', to='locations.garage')),
                ('part_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
            options={
                'unique_together': {('garage', 'part_category')},
            },
        ),
        migrations.CreateModel(
            name='GarageReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('garage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='locations.garage')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('garage', 'user')},
            },
        ),
    ]
