from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from notifications.views import (
		all_note,
		get_notifications_ajax,
		read,
	)

urlpatterns = [
	url(r'^$', all_note, name='notifications_all'),
    url(r'^ajax/$', get_notifications_ajax, name='get_notifications_ajax'),
    url(r'^(?P<id>\d+)/$', read, name='notifications_read'),
]