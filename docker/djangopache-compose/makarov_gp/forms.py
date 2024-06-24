from django import forms
import random
from django.utils.translation import get_language

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form. control', 'id': 'email', 'placeholder': 'Your Email'}))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'subject', 'placeholder': 'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Message'}))


class UserCreationForm(forms.Form):

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}),
        max_length=100,
        label='First Name',
        help_text='Enter your first name.'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}),
        max_length=100,
        label='Last Name',
        help_text='Enter your last name.'
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-100'}),
        max_length=100,
        label='Username',
        help_text='Enter your desired username.'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-100'}),
        label='Email',
        help_text='Enter a valid email address.'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}),
        label='Password',
        help_text='Enter a strong password.'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-100'}),
        label='Confirm Password',
        help_text='Enter the same password for verification.'
    )


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Passwords do not match")
        return cleaned_data


class UserModificationForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-75 disabled'}),
        max_length=100,
        label='First Name :',
        help_text='Enter your first name.'
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-75 disabled'}),
        max_length=100,
        label='Last Name :',
        help_text='Enter your last name.'
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'w-75 disabled'}),
        max_length=100,
        label='Username :',
        help_text='Enter your desired username.'
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'w-75 disabled'}),
        label='Email :',
        help_text='Enter a valid email address.'
    )

class AirportForm(forms.Form):
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'nom', 'placeholder': 'Airport Name'}))
    code_pays = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'code_pays', 'placeholder': 'Airport Country Code'}))
    fuseau = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'fuseau', 'placeholder': 'Airport Timezone'}))


class FlightForm(forms.Form):
    date_depart = forms.DateField(label='Date Depart', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    date_arrivee = forms.DateField(label='Date Arrivee', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    heure_depart = forms.TimeField(label='Heure Depart', required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    heure_arrivee = forms.TimeField(label='Heure Arrivee', required=True, widget=forms.TimeInput(attrs={'type': 'time'}))
    prix = forms.DecimalField(label='Prix', required=True, max_digits=10, decimal_places=2)