from django import forms
from django.forms import ModelForm
from .models import Venue, Event



class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        #fields = ('name', 'address', 'zip_code')
        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM',
            'venue': 'Venue',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
            'venue': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Venue'}),
            'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
            'attendees': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Attendees'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
        }

#Create a Venue Form
class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = "__all__"
        #fields = ('name', 'address', 'zip_code')
        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Venue Name'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'address'}),
            'zip_code': forms.TextInput(attrs={'class':'form-control', 'placeholder':'zip code'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder':'phone'}),
            'web': forms.TextInput(attrs={'class':'form-control', 'placeholder':'website'}),
            'email_address': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email'}),
        }
