from django import forms
from .models import Menu

class BookingForm(forms.ModelForm):
    """ form for bookings """
    class Meta:
        model = Menu
        fields = '__all__'