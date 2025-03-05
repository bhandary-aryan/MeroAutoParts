# payment/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('process/<int:order_id>/', views.payment_process, name='payment_process'),
    path('verify/', views.khalti_verify, name='khalti_verify'),
    path('success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('failed/<int:order_id>/', views.payment_failed, name='payment_failed'),
]