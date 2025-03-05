# payment/views.py
import json
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Order
from .models import Payment

@login_required
def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Check if order is already paid
    if hasattr(order, 'payment') and order.payment.status == 'completed':
        messages.info(request, 'This order has already been paid for.')
        return redirect('order_detail', order_id=order.id)
    
    # Create or get payment
    payment, created = Payment.objects.get_or_create(
        order=order,
        user=request.user,
        defaults={
            'amount': order.total_amount,
            'status': 'pending'
        }
    )
    
    context = {
        'order': order,
        'payment': payment,
        'khalti_public_key': settings.KHALTI_CONFIG['PUBLIC_KEY'],
        'return_url': settings.KHALTI_CONFIG['RETURN_URL'],
        'website_url': settings.KHALTI_CONFIG['WEBSITE_URL'],
    }
    
    return render(request, 'payment/process.html', context)

@csrf_exempt
def khalti_verify(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        amount = data.get('amount')
        order_id = data.get('order_id')
        
        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            'token': token,
            'amount': amount
        }
        headers = {
            'Authorization': f"Key {settings.KHALTI_CONFIG['SECRET_KEY']}"
        }
        
        # Verify with Khalti API
        response = requests.post(url, payload, headers=headers)
        
        if response.status_code == 200:
            # Payment successful
            order = get_object_or_404(Order, id=order_id)
            payment = get_object_or_404(Payment, order=order)
            
            # Update payment status
            payment.status = 'completed'
            payment.transaction_id = token
            payment.save()
            
            # Update order status
            order.status = 'processing'  # Change from pending to processing
            order.save()
            
            return JsonResponse({'success': True, 'redirect_url': f'/orders/{order_id}/'})
        
        return JsonResponse({'success': False, 'error': response.text})
    
    return JsonResponse({'error': 'Invalid request method'})

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment/success.html', {'order': order})

def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment/failed.html', {'order': order})