from django.conf import settings
from django.db import models

# Create your models here.

from products.models import Product
from bookings.models import Booking

class Transaction(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	product = models.ForeignKey(Product)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=500.00, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	success = models.BooleanField(default=True)
	# transaction_id_payment_system = Braintree / Stripe
	# payment_method
	# last_four
	
	def __str__(self):
		return "%s" %(self.id)



class TransactionBooking(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	booking = models.ForeignKey(Booking)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=500.00, null=True, blank=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	success = models.BooleanField(default=True)
	# transaction_id_payment_system = Braintree / Stripe
	# payment_method
	# last_four
	
	def __str__(self):
		return "%s" %(self.id) 