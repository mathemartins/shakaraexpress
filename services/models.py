from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# Create your models here.

from shops.models import ShopAccount

sections = (
		('Beauty', 'Beauty'),
		('Fashion', 'Fashion'),
		('Wellness', 'Wellness'),
		('Lifestyle', 'Lifestyle'),
		('Spa', 'Spa')
	)

def download_media_location(instance, filename):
	return "%s/%s" %(instance.slugy, filename)

class ServiceQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)


class ServiceManager(models.Manager):
	def get_queryset(self):
		return ServiceQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	def get_for_user(self, *args, **kwargs):
		return self.get_queryset().active().filter(user=user)[:5]

	def get_related(self, instance):
		services_one = self.get_queryset().filter(categories__in=instance.categories.all())
		services_two = self.get_queryset().filter(default=instance.default)
		qs = (services_one | services_two).exclude(id=instance.id).distinct()
		return qs

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

class Service(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	shop = models.ForeignKey(ShopAccount, on_delete=models.CASCADE, blank=True, null=True)
	title = models.CharField(max_length=120)
	description = models.TextField(blank=True, null=True)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category', blank=True)
	default = models.ForeignKey('Category', related_name='default_category', null=True, blank=True)
	category = models.CharField(choices=sections, max_length=100, default='Beauty')
	slugy = models.SlugField(blank=True)
	display_image = ProcessedImageField(upload_to=download_media_location, processors=[ResizeToFill(500, 500)], format='JPEG', options={'quality':100}, null=True, blank=True)
	featured = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	objects = ServiceManager()

	class Meta:
		ordering = ["-timestamp", "-updated", "-title"]

	def __str__(self): #def __str__(self):
		return self.title 

	def get_absolute_url(self):
		return reverse("service_detail", kwargs={"pk": self.pk})

	def get_image_url(self):
		img = self.serviceimage_set.first()
		if img:
			return img.image.url
		return img #None

from django.db.models.signals import pre_save, post_save

def create_slug(instance, new_slug=None):
	slugy = slugify(instance.title)
	if new_slugy is not None:
		slugy = new_slugy
	qs = Service.objects.filter(slugy=slugy)
	exists = qs.exists()
	if exists:
		new_slugy = "%s-%s" %(slugy, qs.first().id)
		return create_slug(instance, new_slugy=new_slugy)
	return slugy


def service_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slugy:
		instance.slugy = create_slug(instance)
		
pre_save.connect(service_pre_save_receiver, sender=Service)




class Variation(models.Model):
	service = models.ForeignKey(Service)
	title = models.CharField(max_length=120)
	price = models.DecimalField(decimal_places=2, max_digits=20)
	sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True) #refer none == unlimited amount

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sale_price is not None:
			return self.sale_price
		else:
			return self.price

	def get_html_price(self):
		if self.sale_price is not None:
			html_text = "<span class='sale-price'>%s</span> <span class='og-price'>%s</span>" %(self.sale_price, self.price)
		else:
			html_text = "<span class='price'>%s</span>" %(self.price)
		return mark_safe(html_text)

	def get_absolute_url(self):
		return self.service.get_absolute_url()

	def add_to_booking(self):
		return "%s?item=%s&qty=1" %(reverse("booking"), self.id)

	def remove_from_booking(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("booking"), self.id)

	def get_title(self):
		return "%s - %s" %(self.service.title, self.title)



def service_post_saved_receiver(sender, instance, created, *args, **kwargs):
	service = instance
	variations = service.variation_set.all()
	if variations.count() == 0:
		new_var = Variation()
		new_var.service = service
		new_var.title = "Default"
		new_var.price = service.price
		new_var.save()


post_save.connect(service_post_saved_receiver, sender=Service)


def image_upload_to(instance, filename):
	title = instance.service.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "services/%s/%s" %(slug, new_filename)


class ServiceImage(models.Model):
	service = models.ForeignKey(Service)
	image = models.ImageField(upload_to=image_upload_to)

	def __str__(self):
		return self.service.title

# Service Category


class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(null=True, blank=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("category_detail", kwargs={"slug": self.slug })



def image_upload_to_featured(instance, filename):
	title = instance.service.title
	slug = slugify(title)
	basename, file_extension = filename.split(".")
	new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
	return "services/%s/featured/%s" %(slug, new_filename)




class ServiceFeatured(models.Model):
	service = models.ForeignKey(Service)
	image = models.ImageField(upload_to=image_upload_to_featured)
	title = models.CharField(max_length=120, null=True, blank=True)
	text = models.CharField(max_length=220, null=True, blank=True)
	text_right = models.BooleanField(default=False)
	text_css_color = models.CharField(max_length=6, null=True, blank=True)
	show_price = models.BooleanField(default=False)
	make_image_background = models.BooleanField(default=False)
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.service.title










