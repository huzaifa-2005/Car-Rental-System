from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.utils import timezone
from .models import CustomUser,Car

'''UserCreationForm--its a prebuilt Django form 
to create a new user safely, with built-in password confirmation handling.'''

class AdminCarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'seating_capacity', 'rent_per_day','model_year','image']

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'address')
    
class CustomUserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class RentalForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date()
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=timezone.now().date() + timezone.timedelta(days=1)
    )
    pin_code = forms.CharField(
        max_length=6,
        widget=forms.PasswordInput(),
        help_text='Enter your PIN code to confirm rental'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            # Ensure start date is not in the past
            today = timezone.now().date()
            if start_date < today:
                raise forms.ValidationError('Start date cannot be in the past')
            
            # Ensure end date is not before start date
            if end_date < start_date:
                raise forms.ValidationError('End date must be after start date')
        
        return cleaned_data

class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        min_value=0.01,
        help_text='Enter amount to add to your balance'
    )