from django.contrib import admin
from django.db import models

# Register your models here.
from pagedown.widgets import AdminPagedownWidget
from bookings.models import Booking

class BookingModelAdmin(admin.ModelAdmin):
    """docstring for QuestionModelAdmin"""
    list_display = ['__str__', 'shop']
    list_filter = ['shop', 'timestamp']
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget },
    }

    class Meta:
        model = Booking


admin.site.register(Booking, BookingModelAdmin)