from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

from shops.models import ShopAccount

from products.models import Product
from services.models import Service

from newsletter.models import Newsletter
from newsletter.forms import NewsletterModelForm

# Create your views here.

def homepage(request):
	user = request.user
	try:
		obj = ShopAccount.objects.get(user=user)
	except Exception as e:
		obj = None
	if request.user.is_authenticated():
		my_bookings = None
	else:
		my_bookings = None
	print (my_bookings)
	newsletter_form = NewsletterModelForm()
	query = request.GET.get("q")
	query2 = request.GET.get("q2")
	if query and query2:
		if len(query) == 0:
			if len(query2) == 0:
				raise ValidationError("Either fields cannot be empty!")
				qs = qs.filter(
						Q(business_name__icontains=query)|
						Q(profession__icontains=query) |
						Q(category__icontains=query) |
						Q(address__icontains=query2)
					)
	template = "core/index.html"
	context = {
		"obj":obj,
		"newsletter_form":newsletter_form,
		"my_bookings":my_bookings
	}
	return render(request, template, context)


def featured_objects(request):
	featured_shop = ShopAccount.objects.filter(featured=True).filter(active=True).order_by('?')[:10]
	print (featured_shop)
	featured_product = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	print (featured_product)
	featured_service = Service.objects.filter(featured=True).filter(active=True).order_by('?')[:10]
	featured = []
	for obj in featured_shop:
		featured.append(obj)
		print (type(obj))
	for obj_ in featured_product:
		featured.append(obj_)
		print (type(obj))
	for instance in featured_service:
		featured.append(instance)
	template = "core/featured.html"
	context = {
		"featured":featured
	}
	return render (request, template, context)


def nearby_shops(request):
	nearby_ = Service.objects.filter(active=True).order_by('?')[:10]
	nb_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	nearby = []
	for obj in nearby_:
		nearby.append(obj)
	for instance in nb_prod:
		nearby.append(instance) 
	template = "core/nearby.html"
	context = {
		"nearby":nearby
	}
	return render (request, template, context)

def wellness(request):
	wellness_ = Service.objects.filter(active=True).order_by('?')[:10]
	well_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	wellness = []
	for obj in wellness_:
		wellness.append(obj)
	for instance in well_prod:
		wellness.append(instance)
	template = "core/wellness.html"
	context = {
		"wellness":wellness
	}
	return render (request, template, context)


def fashion(request):
	fashion_ = Service.objects.filter(active=True).order_by('?')[:10]
	fash_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	fashion = []
	for obj in fashion_:
		fashion.append(obj)
	for instance in fash_prod:
		fashion.append(instance)
	template = "core/fashion.html"
	context = {
		"fashion":fashion
	}
	return render (request, template, context)


def beauty(request):
	beauty_ = Service.objects.filter(active=True).order_by('?')[:10]
	beau_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	beauty = []
	for obj in beauty_:
		beauty.append(obj)
	for instance in beau_prod:
		beauty.append(instance)
	template = "core/beauty.html"
	context = {
		"beauty":beauty
	}
	return render (request, template, context)


def spa(request):
	spa_ = Service.objects.filter(active=True).order_by('?')[:10]
	spa_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	spa = []
	for obj in spa_:
		spa.append(obj)
	for instance in spa_prod:
		spa.append(instance)
	template = "core/spa.html"
	context = {
		"spa":spa
	}
	return render (request, template, context)

def deal_of_the_day(request):
	dotd_ = Service.objects.filter(active=True).order_by('?')[:10]
	dotd_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	dotd = []
	for deal in dotd_prod:
		if deal.sale_price:
			dotd.append(deal)
	for instance in dotd_:
		dotd.append(instance)
	template = "core/dotd.html"
	context = {
		"dotd":dotd
	}
	return render (request, template, context)

def lifestyle(request):
	lifestyle_ = Service.objects.filter(active=True).order_by('?')[:10]
	lifestyle_prod = Product.objects.filter(featured=True).filter(sale_active=True).order_by('?')[:10]
	lifestyle = []
	for obj in lifestyle_:
		lifestyle.append(obj)
	for instance in lifestyle_prod:
		lifestyle.append(instance)
	template = "core/lifestyle.html"
	context = {
		"lifestyle":lifestyle
	}
	return render ( request, template, context )


