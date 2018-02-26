from django.contrib import admin

# Register your models here.
from bookings.models import Booking, BookingItem



class BookingItemInline(admin.TabularInline):
	model = BookingItem

class BookingAdmin(admin.ModelAdmin):
	inlines = [
		BookingItemInline
	]
	class Meta:
		model = Booking


admin.site.register(Booking, BookingAdmin)