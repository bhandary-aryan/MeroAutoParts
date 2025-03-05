# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Review
from .models import User, Review, Order



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    address1 = forms.CharField(max_length=255, required=True)
    address2 = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'address1', 'address2', 'phone_number')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'address1', 'address2', 'phone_number', 'profile_picture')

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