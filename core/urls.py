# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Email verification URL
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    
    # Password Reset URLs
    path('password-reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='core/password_reset_form.html',
        email_template_name='core/email/password_reset_email.html',
        subject_template_name='core/email/password_reset_subject.txt',
        html_email_template_name='core/email/password_reset_email.html',  # This explicitly sets the HTML template
        success_url='/password-reset/done/'
    ), 
    name='password_reset'),
    
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='core/password_reset_done.html'
        ), 
        name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name='core/password_reset_confirm.html',
            success_url='/password-reset-complete/'
        ), 
        name='password_reset_confirm'),
    
    path('password-reset-complete/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='core/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    
    # Review URLs
    path('add_review/<int:product_id>/', views.add_review, name='add_review'),
    
    # Cart URLs
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),

    # Search URL
    path('search/', views.search_products, name='search_products'),

    # Checkout and Order URLs
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),

    # Buy Now URL
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
]