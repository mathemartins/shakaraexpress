from django import forms
from pagedown.widgets import PagedownWidget
from bookings.models import Booking

class BookingForm(forms.ModelForm):
    """docstring for QuestionForm"""
    class Meta:
        model = Booking
        fields = [
            # "shop",
            "optional_names",
            "mobile_contact",
            "booking_date",
            "extra_notes",
            "promotional_code"
        ]
        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
