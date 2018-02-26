from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete


from services.models import Variation
from shops.models import ShopAccount
# Create your models here.


class BookingItem(models.Model):
	booking = models.ForeignKey("Booking")
	item = models.ForeignKey(Variation)
	quantity = models.PositiveIntegerField(default=1)
	line_item_total = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.item.title

	def remove(self):
		return self.item.remove_from_booking()


def booking_item_pre_save_receiver(sender, instance, *args, **kwargs):
	qty = instance.quantity
	qty = int(qty)
	if qty >= 1:
		price = instance.item.get_price()
		line_item_total = Decimal(qty) * Decimal(price)
		instance.line_item_total = line_item_total

pre_save.connect(booking_item_pre_save_receiver, sender=BookingItem)



def booking_item_post_save_receiver(sender, instance, *args, **kwargs):
	instance.booking.update_subtotal()

post_save.connect(booking_item_post_save_receiver, sender=BookingItem)

post_delete.connect(booking_item_post_save_receiver, sender=BookingItem)


class Booking(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True)
	shop = models.ForeignKey(ShopAccount, null=True, blank=True)
	items = models.ManyToManyField(Variation, through=BookingItem)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
	tax_percentage  = models.DecimalField(max_digits=10, decimal_places=5, default=0.05)
	tax_total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)
	total = models.DecimalField(max_digits=50, decimal_places=2, default=25.00)

	def __str__(self):
		return str(self.id)

	def update_subtotal(self):
		print ("updating...")
		subtotal = 0
		items = self.bookingitem_set.all()
		for item in items:
			subtotal += item.line_item_total
		self.subtotal = "%.2f" %(subtotal)
		self.save()




def do_tax_and_total_receiver(sender, instance, *args, **kwargs):
	subtotal = Decimal(instance.subtotal)
	tax_total = round(subtotal * Decimal(instance.tax_percentage), 2) #8.5%
	print (instance.tax_percentage)
	total = round(subtotal + Decimal(tax_total), 2)
	instance.tax_total = "%.2f" %(tax_total)
	instance.total = "%.2f" %(total)
	#instance.save()



pre_save.connect(do_tax_and_total_receiver, sender=Booking)









