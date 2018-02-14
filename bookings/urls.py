from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from bookings.views import (
	bookings_detail,
	booking_update
)

urlpatterns = [
	url(r'^(?P<pk>\d+)/detail/$', bookings_detail, name='booking_detail'),
	url(r'^(?P<pk>\d+)/detail/edit/$', booking_update, name='booking_update'),
]