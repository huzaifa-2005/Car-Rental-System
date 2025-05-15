from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.utils import timezone
from .models import CustomUser,Car

'''UserCreationForm--its a prebuilt Django form 
to create a new user safely, with built-in password confirmation handling.'''

''' The Meta class inside our class based forms tells Django how to build the form from the model by providing 
        configuration like which model and fields to use. '''

class AdminCarForm(forms.ModelForm): # for admin_add_car view
    class Meta:
        
        model = Car
        fields = ['name', 'brand', 'seating_capacity', 'rent_per_day','model_year','image']
        # fields defines the model's fields to be included in the form.
        # exclude defines the model's fields to be excluded from the form.

class CustomUserCreationForm(UserCreationForm):  # for signup_view
    # custom first_name and last_name fields because max_length by default is 150
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'address')
    
class CustomUserLoginForm(forms.Form):   # for login_view
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

# class RentalForm(forms.Form):  # for car_detail_view
    # start_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     initial=timezone.now().date()
    # )
    # end_date = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     initial=timezone.now().date() + timezone.timedelta(days=1)
    # )
   
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     start_date = cleaned_data.get('start_date')
    #     end_date = cleaned_data.get('end_date')
        
    #     if start_date and end_date:
    #         # Ensure start date is not in the past
    #         today = timezone.now().date()
    #         if start_date < today:
    #             raise forms.ValidationError('Start date cannot be in the past')
            
    #         # Ensure end date is not before start date
    #         if end_date < start_date:
    #             raise forms.ValidationError('End date must be after start date')
        
    #     return cleaned_data

class AddBalanceForm(forms.Form):  # for profile_view (when user wants to add balance)
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=None,
        min_value=1,
        help_text='Enter amount to add to your balance'
    )