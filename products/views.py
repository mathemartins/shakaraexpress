import os

from mimetypes import guess_type

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

# Create your views here.
from analytics.models import TagView
from dev.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin, 
			SubmitBtnMixin,
			AjaxRequiredMixin
		)

from shops.models import ShopAccount
from shops.mixins import ShopAccountMixin
from tags.models import Tag

from products.forms import ProductAddForm, ProductModelForm
from products.mixins import ProductManagerMixin
from products.models import Product


class ProductCreateView(ShopAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		shop = self.get_account()
		form.instance.shop = shop
		valid_data = super(ProductCreateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		if tags:
			tags_list = tags.split(",")
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(form.instance)
		return valid_data


class ProductUpdateView(ProductManagerMixin, SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Update Product"

	def get_initial(self):
		initial = super(ProductUpdateView,self).get_initial()
		tags = self.get_object().tag_set.all()
		initial["tags"] = ", ".join([x.title for x in tags])
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		print (initial)
		return initial

	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		tags = form.cleaned_data.get("tags")
		obj = self.get_object()
		obj.tag_set.clear()
		if tags:
			tags_list = tags.split(",")
			
			for tag in tags_list:
				if not tag == " ":
					new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
					new_tag.products.add(self.get_object())
		return valid_data

	

class ProductDetailView(MultiSlugMixin, DetailView):
	model = Product

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		tags = obj.tag_set.all()
		if self.request.user.is_authenticated():
			for tag in tags:
				new_view = TagView.objects.add_count(self.request.user, tag)
		return context


class ShopProductListView(ShopAccountMixin, ListView):
	model = Product
	template_name = "shops/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(ShopProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(shop=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs
	

class ProductListView(ListView):
	model = Product

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(sale_active=True)
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(title__icontains=query)|
					Q(description__icontains=query)
				).order_by("title")
		return qs


def create_view(request): 
	form = ProductModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
			"form": form,
			"submit_btn": "Create Product"
		}
	return render(request, template, context)


def update_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	form = ProductModelForm(request.POST or None, instance=product)
	if form.is_valid():
		instance = form.save(commit=False)
		#instance.sale_price = instance.price
		instance.save()
	template = "form.html"
	context = {
		"object": product,
		"form": form,
		"submit_btn": "Update Product"
		}
	return render(request, template, context)



def detail_slug_view(request, slug=None):
	product = Product.objects.get(slug=slug)
	try:
		product = get_object_or_404(Product, slug=slug)
	except Product.MultipleObjectsReturned:
		product = Product.objects.filter(slug=slug).order_by("-title").first()
	# print slug
	# product = 1
	template = "detail_view.html"
	context = {
		"object": product
		}
	return render(request, template, context)


def detail_view(request, object_id=None):
	product = get_object_or_404(Product, id=object_id)
	template = "detail_view.html"
	context = {
		"object": product
		}
	return render(request, template, context)

	# if object_id is not None:
	# 	product = get_object_or_404(Product, id=object_id)
	# 	# product = Product.objects.get(id=object_id)
	# 	# try:
	# 	# 	product = Product.objects.get(id=object_id)
	# 	# except Product.DoesNotExist:
	# 	# 	product = None

		
	# else:
	# 	raise Http404


def list_view(request):
	# list of items
	queryset = Product.objects.all()
	template = "list_view.html"
	context = {
		"queryset": queryset
	}
	return render(request, template, context)




