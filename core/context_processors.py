# core/context_processors.py
from .models import Cart

def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return {'user_cart': cart}
    return {'user_cart': None}