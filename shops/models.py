from __future__ import unicode_literals
import random
import string

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.db import models

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from markdown_deux import markdown

# Create your models here.


class Profession(models.Model):
	profession = models.CharField(max_length=200)
	active = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return "%s" % self.profession

sections = (
		('Beauty', 'Beauty'),
		('Fashion', 'Fashion'),
		('Wellness', 'Wellness'),
		('Lifestyle', 'Lifestyle')
	)


def upload_location(instance, filename):
    # creates an instance id folder
    # for storing images wrt shopaccount_id
    return "%s/%s" %(instance.id, filename)


class ShopAccount(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="manager_workers", blank=True)
	business_name = models.CharField(max_length=200)
	shop_description = models.TextField(null=True, blank=True)
	dashboard_banner_image_1 = models.ImageField(upload_to = upload_location, null = True, blank = True)
	user_image = ProcessedImageField(upload_to=upload_location, processors=[ResizeToFill(150, 150)], 
								format='JPEG', options={'quality':100}, null=True, blank=True)
	work_image = ProcessedImageField(upload_to=upload_location, processors=[ResizeToFill(300, 150)], 
								format='JPEG', options={'quality':100}, null=True, blank=True)
	profession = models.OneToOneField(Profession, on_delete=models.CASCADE, primary_key=True)
	category = models.CharField(choices=sections, max_length=100)
	let_client_book_online = models.BooleanField(default=False)
	address = models.CharField(max_length=200)
	map_embed = models.CharField(max_length=200, blank=True, null=True)
	cancellation_policy = models.TextField()
	mobile_number = models.CharField(max_length=11)
	active = models.BooleanField(default=False)
	slug = models.SlugField(null=True, blank=True)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	class Meta:
		ordering = ["-timestamp", "-updated"]


	def __str__(self):
		return str(self.business_name)

	def get_absolute_url(self):
		return reverse("shop:shop-detail", kwargs={'slug':self.slug})

	def get_markdown_content(self):
		shop_description = self.shop_description
		markdown_text = markdown(shop_description)
		return mark_safe(markdown_text)

	def cancel_markdown(self):
		cancellation_policy = self.cancellation_policy
		markdown_text = markdown(cancellation_policy)
		return mark_safe(markdown_text)


def shopaccount_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.business_name)
		new_slug = "%s %s" %(instance.business_name, instance.pk)
		try:
			slug_exists = ShopAccount.objects.get(slug=instance.slug)
			instance.slug = slugify(new_slug)
			print ("models exists, new_slug generated")
		except ShopAccount.DoesNotExist:
			instance.slug = instance.slug
			print ("slug created")
		except ShopAccount.MultipleObjectsReturned:
			instance.slug = slugify(new_slug)
			print ("multiple models already exists, new slug generated")
		except:
			pass

pre_save.connect(shopaccount_pre_save_reciever, sender=ShopAccount)