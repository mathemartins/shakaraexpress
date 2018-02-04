from django import forms
from pagedown.widgets import PagedownWidget
from django.contrib.admin import widgets
from django.forms import DateTimeField
from django.conf import settings
from bookings.models import Booking


class BookingForm(forms.ModelForm):
    """docstring for QuestionForm"""
    # booking_date = forms.SplitDateTimeField(widget=widgets.AdminSplitDateTime())
    # booking_date = DateTimeField(input_formats=["%d %b %Y %H:%M:%S %Z"])


    class Meta:
        model = Booking
        fields = [
            # "shop",
            "service",
            "optional_names",
            "mobile_contact",
            "booking_date",
            "mode_of_payment",
            "extra_notes",
            "promotional_code"
        ]

        widgets = {
            'booking_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

        # 'booking_date': forms.DateTimeField(required=True, input_formats = '%Y-%m-%dT%H:%M')

        def cleaned_date(self):
            booking_date = self.cleaned_data.get("booking_date")
            return  booking_date
        
    
