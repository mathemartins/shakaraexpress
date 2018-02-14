from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

from shops.models import ShopAccount

from products.models import Product

from bookings.models import Booking

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
		my_bookings = Booking.objects.get_for_user(request.user)
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
	featured = []
	for obj in featured_shop:
		featured.append(obj)
		print (type(obj))
	for obj_ in featured_product:
		featured.append(obj_)
		print (type(obj))
	template = "core/featured.html"
	context = {
		"featured":featured
	}
	return render (request, template, context)


def nearby_shops(request):
	nearby = ShopAccount.objects.filter(active=True).order_by('?')[:20]
	template = "core/nearby.html"
	context = {
		"nearby":nearby
	}
	return render (request, template, context)

def wellness(request):
	cat_well = ShopAccount.objects.filter(active=True).filter(category="wellness").order_by('?')[:20]
	print (cat_well)
	template = "core/wellness.html"
	context = {
		"wellness":wellness
	}
	return render (request, template, context)


def fashion(request):
	cat_well = ShopAccount.objects.filter(active=True).filter(category="fashion").order_by('?')[:20]
	print (cat_well)
	template = "core/fashion.html"
	context = {
		"fashion":fashion
	}
	return render (request, template, context)


def beauty(request):
	cat_well = ShopAccount.objects.filter(active=True).filter(category="beauty").order_by('?')[:20]
	print (cat_well)
	template = "core/beauty.html"
	context = {
		"beauty":beauty
	}
	return render (request, template, context)


def spa(request):
	cat_well = ShopAccount.objects.filter(active=True).filter(category="spa").order_by('?')[:20]
	print (cat_well)
	template = "core/spa.html"
	context = {
		"spa":spa
	}
	return render (request, template, context)

def deal_of_the_day(request):
	product = Product.objects.filter(sale_active=True).order_by('?')[:20]
	dotd = []
	for deal in product:
		if deal.sale_price:
			dotd.append(deal)
	template = "core/dotd.html"
	context = {
		"dotd":dotd
	}
	return render (request, template, context)

def lifestyle(request):
	lifestyle_ = ShopAccount.objects.filter(active=True).filter(category="lifestyle").order_by("?")[::20]
	template = "core/lifestyle.html"
	context = {
		"lifestyle":lifestyle
	}
	return render ( request, template, context )


