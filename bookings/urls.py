from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from bookings.views import (
	bookings,
	bookings_detail
	)

urlpatterns = [
	url(r'^all/$', bookings, name='all-bookings'),
	url(r'^(?P<pk>\d+)/detail/$', bookings_detail, name='booking_detail'),
]