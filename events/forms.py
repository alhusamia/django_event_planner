from django import forms
from django.contrib.auth.models import User
from .models import Event,Booking,Profile

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }
class Date(forms.DateInput):
    input_type ="date"
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']
        widgets={
            'birth_date':Date(),

        }



class Time(forms.TimeInput):
    input_type='time'

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['user',]
        widgets={
            'date':Date(),
            'time':Time()
        }

class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
class ReserveForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [ 'reserved_num']
