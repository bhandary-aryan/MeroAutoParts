# from django.contrib import admin
# from django import forms
# from django.db.models import Sum, Count
# from django.urls import path
# from django.shortcuts import render
# from django.utils.html import format_html
# from .models import User, Category, Product, Review, Cart, CartItem, Order, OrderItem

# # Custom admin site
# class MeroAutoPartsAdminSite(admin.AdminSite):
#     site_header = 'MeroAutoParts Administration'
#     site_title = 'MeroAutoParts Admin'
#     index_title = 'Dashboard'
    
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
#         ]
#         return custom_urls + urls
    
#     def dashboard_view(self, request):
#         # Get counts for dashboard
#         user_count = User.objects.count()
#         product_count = Product.objects.count()
#         order_count = Order.objects.count()
#         total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
#         # Get recent orders
#         recent_orders = Order.objects.order_by('-created_at')[:5]
        
#         # Get top selling products
#         top_products = Product.objects.annotate(
#             sold=Count('orderitem')
#         ).order_by('-sold')[:5]
        
#         context = {
#             'user_count': user_count,
#             'product_count': product_count,
#             'order_count': order_count,
#             'total_revenue': total_revenue,
#             'recent_orders': recent_orders,
#             'top_products': top_products,
#             **self.each_context(request),
#         }
#         return render(request, 'admin/dashboard.html', context)
    
#     def index(self, request, extra_context=None):
#         # Add stats to the admin index page
#         user_count = User.objects.count()
#         product_count = Product.objects.count()
#         order_count = Order.objects.count()
#         total_revenue = Order.objects.filter(status='delivered').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        
#         extra_context = extra_context or {}
#         extra_context.update({
#             'user_count': user_count,
#             'product_count': product_count,
#             'order_count': order_count,
#             'total_revenue': total_revenue,
#         })
#         return super().index(request, extra_context)

# # Create the custom admin site instance
# admin_site = MeroAutoPartsAdminSite(name='myadmin')

# # Define the admin classes
# class ProductAdminForm(forms.ModelForm):
#     description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    
#     class Meta:
#         model = Product
#         fields = '__all__'

# class ProductAdmin(admin.ModelAdmin):
#     form = ProductAdminForm
#     list_display = ('image_preview', 'name', 'brand', 'category', 'price', 'stock', 'created_at')
#     list_filter = ('category', 'brand', 'created_at')
#     search_fields = ('name', 'brand', 'model_no', 'description')
#     prepopulated_fields = {'slug': ('name',)}
#     readonly_fields = ('created_at', 'updated_at', 'image_preview')
#     fieldsets = (
#         ('Basic Information', {
#             'fields': ('name', 'slug', 'brand', 'model_no', 'category', 'price', 'stock', 'image', 'image_preview')
#         }),
#         ('Description', {
#             'fields': ('description',)
#         }),
#         ('Metadata', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )
    
#     def image_preview(self, obj):
#         if obj.image:
#             return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
#         return "No Image"
    
#     image_preview.short_description = 'Preview'
    
#     def get_readonly_fields(self, request, obj=None):
#         if obj:  # editing an existing object
#             return self.readonly_fields
#         return ('created_at', 'updated_at')

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug', 'get_product_count')
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name', 'description')
    
#     def get_product_count(self, obj):
#         return obj.products.count()
    
#     get_product_count.short_description = 'Products'

# class ReviewAdmin(admin.ModelAdmin):
#     list_display = ('product', 'user', 'rating', 'created_at')
#     list_filter = ('rating', 'created_at')
#     search_fields = ('comment', 'user__username', 'product__name')
#     readonly_fields = ('created_at',)

# class CartItemInline(admin.TabularInline):
#     model = CartItem
#     extra = 0
#     raw_id_fields = ('product',)

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('user', 'created_at', 'updated_at', 'get_total_price', 'get_total_items')
#     list_filter = ('created_at', 'updated_at')
#     search_fields = ('user__username',)
#     inlines = [CartItemInline]
#     readonly_fields = ('created_at', 'updated_at')

# class OrderItemInline(admin.TabularInline):
#     model = OrderItem
#     extra = 0
#     raw_id_fields = ('product',)
#     readonly_fields = ('product', 'price', 'quantity')

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'full_name', 'email', 'created_at', 'status', 'total_amount')
#     list_filter = ('status', 'created_at')
#     search_fields = ('full_name', 'email', 'id')
#     inlines = [OrderItemInline]
#     readonly_fields = ('created_at', 'updated_at', 'total_amount')
#     list_editable = ('status',)
#     fieldsets = (
#         ('Customer Information', {
#             'fields': ('user', 'full_name', 'email', 'phone')
#         }),
#         ('Shipping Information', {
#             'fields': ('address', 'city')
#         }),
#         ('Order Details', {
#             'fields': ('status', 'total_amount', 'created_at', 'updated_at')
#         }),
#     )

# # Register models with the standard admin site
# admin.site.register(User)
# admin.site.register(Category, CategoryAdmin)
# admin.site.register(Product, ProductAdmin)
# admin.site.register(Review, ReviewAdmin)
# admin.site.register(Cart, CartAdmin)
# admin.site.register(Order, OrderAdmin)

# # Optionally, you can register with your custom admin site as well
# # but this requires additional URL configuration
# # admin_site.register(User)
# # admin_site.register(Category, CategoryAdmin)
# # admin_site.register(Product, ProductAdmin)
# # admin_site.register(Review, ReviewAdmin)
# # admin_site.register(Cart, CartAdmin)
# # admin_site.register(Order, OrderAdmin)


from django.contrib import admin
from .models import User, Category, Product, Review, Cart, CartItem, Order, OrderItem



# Just register the models without any customization
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)