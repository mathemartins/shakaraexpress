import random

from django.views.generic import View
from django.shortcuts import render

# Create your views here.

from products.models import Product, CuratedProducts

class DashboardView(View):
	def get(self, request, *args, **kwargs):
		tag_views = None
		products = None
		top_tags = None
		curated = CuratedProducts.objects.filter(active=True).order_by("?")
		try:
			tag_views = request.user.tagview_set.all().order_by("-count")[:5]
		except:
			pass

		if tag_views:
			top_tags = [x.tag for x in tag_views]
			products = Product.objects.filter(tag__in=top_tags)

			if products.count() < 10:
				products = Product.objects.all().order_by("?")
				products = products[:10]
			else:
				products = products.distinct()
				products = sorted(products, key= lambda x: random.random())

		context = {
			"products": products,
			"top_tags": top_tags,
			"curated": curated
		}
		return render(request, "dashboard/view.html", context)