# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Review, Order
import re
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        help_text="Enter your full name",
        widget=forms.TextInput(attrs={'placeholder': 'John Doe'})
    )
    email = forms.EmailField(
        max_length=254, 
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'placeholder': 'example@email.com'})
    )
    address1 = forms.CharField(max_length=255, required=True)
    address2 = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'address1', 'address2', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email already exists")
        
        # Basic email pattern validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Please enter a valid email address")
        
        # Check for disposable email domains
        disposable_domains = [
            'mailinator.com', 'yopmail.com', 'tempmail.com', 'temp-mail.org',
            'fakeinbox.com', 'guerrillamail.com', 'sharklasers.com', 'spam4.me'
        ]
        
        domain = email.split('@')[1].lower()
        if domain in disposable_domains:
            raise ValidationError("Please use a permanent email address, not a temporary one")
        
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        # Split full name into first_name and last_name for User model
        full_name_parts = self.cleaned_data["full_name"].split(' ', 1)
        user.first_name = full_name_parts[0]
        if len(full_name_parts) > 1:
            user.last_name = full_name_parts[1]
        
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        help_text="Enter your full name"
    )
    
    class Meta:
        model = User
        fields = ('username', 'full_name', 'email', 'address1', 'address2', 'phone_number', 'profile_picture')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate full_name field if user has first/last name
        if self.instance and self.instance.pk:
            if self.instance.first_name or self.instance.last_name:
                self.fields['full_name'].initial = f"{self.instance.first_name} {self.instance.last_name}".strip()
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Split full name into first_name and last_name
        full_name_parts = self.cleaned_data.get("full_name", "").split(' ', 1)
        user.first_name = full_name_parts[0]
        if len(full_name_parts) > 1:
            user.last_name = full_name_parts[1]
        
        if commit:
            user.save()
        return user

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone', 'address', 'city')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }