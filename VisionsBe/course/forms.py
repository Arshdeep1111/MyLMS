from django import forms
from django.core.exceptions import ValidationError
from django.forms import fields, widgets
from .models import *

class UserUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        def __init__(self):
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['username'].required = True


class UserCreateForm(forms.ModelForm):
    phone = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
        widgets = {'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        def __init__(self):
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['email'].required = True
            self.fields['username'].required = True
            self.fields['password1'].required = True
            self.fields['password2'].required = True
        


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'rating']
        RATING_CHOICES=[
        (20, 1),
        (40, 2),
        (60, 3),
        (80, 4),
        (100, 5)
        ]
        widgets = {'rating': forms.RadioSelect(choices=RATING_CHOICES)}

class WishlistForm(forms.ModelForm):
    class Meta: 
        model = Wishlist
        fields = ['user', 'course']
        widgets = {
        'user': forms.HiddenInput(),
        'course': forms.HiddenInput()
        }
    
    def __init__(self, *args, **kwargs):
        super(WishlistForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['course'].required=False

class FavouriteForm(forms.ModelForm):
    class Meta: 
        model = Favourite
        fields = ['user', 'course']
        widgets = {
        'user': forms.HiddenInput(),
        'course': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(FavouriteForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['course'].required=False

class MyCourseForm(forms.ModelForm):
    class Meta: 
        model = My_course
        fields = ['user', 'course']
        widgets = {
        'user': forms.HiddenInput(),
        'course': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(MyCourseForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['course'].required=False
    

class CartForm(forms.ModelForm):
    coupon = forms.CharField(max_length=25, required=False)
    class Meta: 
        model = Cart
        fields = ['user', 'course', 'amount']
        widgets = {
        'user': forms.HiddenInput(),
        'course': forms.HiddenInput(),
        'amount':forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['course'].required=False
        self.fields['amount'].required=False
    
    def save(self, commit = True):
        coupon_code = self.cleaned_data['coupon']
        if coupon_code:
            try:
                coupon_obj = Coupon.objects.get(code=coupon_code, course=self.fields['course'])
            except:
                raise ValidationError('Invalid Coupon Code')
            else:
                self.instance.coupon=coupon_obj
        else:
            self.instance.coupon = None
        return super().save(commit=commit)

