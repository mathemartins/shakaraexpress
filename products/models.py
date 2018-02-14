from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
# Create your models here.

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from shops.models import ShopAccount


def download_media_location(instance, filename):
	return "%s/%s" %(instance.slug, filename)

class Product(models.Model):
	shop = models.ForeignKey(ShopAccount)
	managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
	media = ProcessedImageField(upload_to=download_media_location, processors=[ResizeToFill(500, 500)], format='JPEG', options={'quality':100}, null=True, blank=True)
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True, unique=True)
	description = models.TextField()
	quantity_available = models.IntegerField(blank=True, null=True)
	price = models.DecimalField(max_digits=100, decimal_places=2, default=500.00, null=True, blank=True) #100.00
	sale_active = models.BooleanField(default=False)
	sale_price = models.DecimalField(max_digits=100,
			 decimal_places=2, default=500.00, null=True, blank=True) #100.00
	featured = models.BooleanField(default=False)

	def __str__(self): #def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		view_name = "products:detail_slug"
		return reverse(view_name, kwargs={"slug": self.slug})

	def get_edit_url(self):
		view_name = "shop:product_edit"
		return reverse(view_name, kwargs={"pk": self.pk})

	@property
	def get_price(self):
		if self.sale_price and self.sale_active:
			return self.sale_price
		return self.price

	def get_html_price(self):
		price = self.get_price
		if price == self.sale_price:
			return "<p><span>%s</span> <span style='color:red;text-decoration:line-through;'>%s</span></p>" %(self.sale_price, self.price)
		else:
			return "<p>%s</p>" %(self.price)


def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Product.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
		
pre_save.connect(product_pre_save_receiver, sender=Product)


class CuratedProducts(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	section_name = models.CharField(max_length=120)
	products = models.ManyToManyField(Product, blank=True)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.section_name

