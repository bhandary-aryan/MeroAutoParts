# core/views.py
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm, UserUpdateForm, User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Product, Review, Cart, CartItem
from .forms import ReviewForm
from django.db import models
from .models import Category, Product, Review, Cart, CartItem, Order, OrderItem
from .forms import SignUpForm, LoginForm, UserUpdateForm, ReviewForm, CheckoutForm

# Email verification imports
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage


def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.all()[:6]  # Get 6 products for the homepage
    return render(request, 'core/home.html', {
        'categories': categories,
        'featured_products': featured_products
    })

def signup(request):
    try:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                
                # Skip email verification for now
                user.email_verified = True
                user.save()
                
                login(request, user)
                messages.success(request, "Registration successful! Welcome to MeroAutoParts.")
                return redirect('home')
        else:
            form = SignUpForm()
        
        return render(request, 'core/signup.html', {'form': form})
    
    except Exception as e:
        print(f"Error in signup view: {e}")
        messages.error(request, "An error occurred during signup. Please try again.")
        return redirect('signup')
    

def send_verification_email(request, user):
    """Send an email verification link to the user"""
    token = user.generate_verification_token()
    
    current_site = get_current_site(request)
    mail_subject = 'Activate your MeroAutoParts account'
    message = render_to_string('core/email/account_verification_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': token,
    })
    
    to_email = user.email
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"
    email.send()

def verify_email(request, uidb64, token):
    """Handle email verification link"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and user.verification_token == token:
        user.email_verified = True
        user.verification_token = None
        user.save()
        
        login(request, user)
        messages.success(request, 'Your email has been verified! Your account is now active.')
        return redirect('home')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('home')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if email is verified
                if hasattr(user, 'email_verified') and not user.email_verified:
                    messages.warning(request, 'Please verify your email address before logging in. Check your inbox for the verification link.')
                    return redirect('login')
                
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'core/profile.html', {'form': form})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    
    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Brand filter
    brand = request.GET.get('brand')
    if brand:
        products = products.filter(brand=brand)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Get all available brands for filter
    all_brands = Product.objects.values_list('brand', flat=True).distinct()
    
    return render(request, 'core/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'all_brands': all_brands,
    })

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)
    reviews = product.reviews.all()
    review_form = ReviewForm()
    
    # Check if the user has already reviewed this product
    user_has_reviewed = False
    if request.user.is_authenticated:
        user_has_reviewed = reviews.filter(user=request.user).exists()
    
    return render(request, 'core/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'user_has_reviewed': user_has_reviewed
    })

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if user already reviewed this product
            if product.reviews.filter(user=request.user).exists():
                messages.error(request, 'You have already reviewed this product.')
                return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)
            
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added.')
            return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)
    
    return redirect('product_detail', category_slug=product.category.slug, product_slug=product.slug)

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'core/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if the product is already in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        # If the item already exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name} added to your cart.')
    
    # Check if this is a Buy Now action (redirect to checkout) or regular Add to Cart
    if request.POST.get('buy_now'):
        return redirect('checkout')
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'{product_name} removed from your cart.')
    return redirect('cart_detail')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart_detail')

def search_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        models.Q(name__icontains=query) | 
        models.Q(description__icontains=query) |
        models.Q(brand__icontains=query) |
        models.Q(model_no__icontains=query)
    )
    
    return render(request, 'core/product_list.html', {
        'products': products,
        'query': query,
        'categories': Category.objects.all()
    })

@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        messages.error(request, "You don't have any items in your cart.")
        return redirect('cart_detail')
    
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    price=cart_item.product.price,
                    quantity=cart_item.quantity
                )
                
                # Update product stock
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # Clear the cart
            cart.items.all().delete()
            
            messages.success(request, f"Your order has been placed successfully!")
            
            # Redirect to payment page
            return redirect('payment_process', order_id=order.id)
    else:
        # Pre-fill the form with user information
        full_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
        initial_data = {
            'full_name': full_name,
            'email': request.user.email,
            'phone': request.user.phone_number,
            'address': request.user.address1,
            'city': '',
        }
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'core/checkout.html', {
        'form': form,
        'cart': cart
    })

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Create or get user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Clear the cart (since we're buying just this product)
    cart.items.all().delete()
    
    # Add the product to cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity = 1  # Set quantity to 1 for Buy Now
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart. Proceed to checkout.")
    
    # Redirect directly to checkout
    return redirect('checkout')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_list.html', {'orders': orders})