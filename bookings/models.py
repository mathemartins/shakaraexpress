from __future__ import unicode_literals
import random
import string

from django.db import models
from django.conf import settings
from django.template.defaultfilters import truncatechars
from django.utils.text import Truncator
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from markdown_deux import markdown

# Create your models here.
from shops.models import ShopAccount, Service
from bookings.utils import (
	booking_code_generator, 
	statistics_average_calculator, 
	get_read_time,
)

pay_style = (
        ('card', 'card'),
        ('cash', 'cash'),
    )

class BookingManager(models.Manager):
    """docstring for BookingManager"""
    def all(self):
        return super(BookingManager, self).filter(active=True)

    def recent(self):
        try:
        	limit_to = settings.RECENT_BOOKING_NUMBER
        except:
        	limit_to = 10
        return self.get_queryset().filter(active=True)[:limit_to]

    def get_for_shop(self, shop):
        return self.get_queryset().filter(active=True).filter(shop=shop)

    def get_for_user(self, user):
        return self.get_queryset().filter(active=True).filter(user=user)[:5]
        

class Booking (models.Model):
    """docstring for Question"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    destination = models.CharField(max_length=200, blank=True, null=True)
    service = models.ManyToManyField(Service, related_name="select_services", blank=True)
    shop = models.ForeignKey(ShopAccount, null=True, blank=True)
    booking_date = models.DateTimeField(null=True, blank=True)
    mobile_contact = models.CharField(max_length=11, blank=True, null=True)
    optional_names = models.CharField(max_length=100, blank=True, null=True)
    promotional_code = models.CharField(max_length=50, blank=True, null=True)
    extra_notes = models.TextField(blank=True, null=True)
    booking_code = models.CharField(max_length=5, blank=True, null=True)
    mode_of_payment = models.CharField(choices=pay_style, max_length=100)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = BookingManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.booking_code)

    def get_absolute_url(self):
        return reverse('book:booking_detail', kwargs={'pk':self.pk})

    # def get_booking_as_markdown(self):
    #     content = self.text
    #     markdown_text = markdown(content)
    #     return mark_safe(markdown_text)

    @property
    def get_instance_location(self):
        return self.destination

    # @property
    # def get_preview(self):
    #     return truncatechars(self.text, 100)
    #     #return Truncator(self.text).char(100)

    @property
    def get_booking(self):
        return self.booking_code