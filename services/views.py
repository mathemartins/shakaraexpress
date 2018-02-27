from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone


from django_filters import FilterSet, CharFilter, NumberFilter
# Create your views here.

from services.forms import VariationInventoryFormSet, ServiceFilterForm
from services.mixins import StaffRequiredMixin
from services.models import Service, Variation, Category

from shops.models import ShopAccount



class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "services/service_list.html"


class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		service_set = obj.service_set.all()
		default_services = obj.default_category.all()
		services = ( service_set | default_services ).distinct()
		context["services"] = services
		return context



class VariationListView(StaffRequiredMixin, ListView):
	model = Variation
	queryset = Variation.objects.all()

	def get_context_data(self, *args, **kwargs):
		context = super(VariationListView, self).get_context_data(*args, **kwargs)
		context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
		return context

	def get_queryset(self, *args, **kwargs):
		service_pk = self.kwargs.get("pk")
		if service_pk:
			service = get_object_or_404(Service, pk=service_pk)
			queryset = Variation.objects.filter(service=service)
		return queryset

	def post(self, request, *args, **kwargs):
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				#if new_item.title:
				service_pk = self.kwargs.get("pk")
				service = get_object_or_404(Service, pk=service_pk)
				new_item.service = service
				new_item.save()
				
			messages.success(request, "Your inventory and pricing has been updated.")
			return redirect("services")
		raise Http404



class ServiceFilter(FilterSet):
	title = CharFilter(name='title', lookup_type='icontains', distinct=True)
	category = CharFilter(name='categories__title', lookup_type='icontains', distinct=True)
	category_id = CharFilter(name='categories__id', lookup_type='icontains', distinct=True)
	min_price = NumberFilter(name='variation__price', lookup_type='gte', distinct=True) # (some_price__gte=somequery)
	max_price = NumberFilter(name='variation__price', lookup_type='lte', distinct=True)
	class Meta:
		model = Service
		fields = [
			'min_price',
			'max_price',
			'category',
			'title',
			'description',
		]


def service_list(request):
	qs = Service.objects.all()
	ordering = request.GET.get("ordering")
	if ordering:
		qs = Service.objects.all().order_by(ordering)
	# f = ServiceFilter(request.GET, queryset=qs)
	# f = list(f)
	return render(request, "services/service_list.html", {"object_list": qs })


class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a queryset in order to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering:
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context




class ServiceListView(FilterMixin, ListView):
	model = Service
	queryset = Service.objects.all()
	# filter_class = ServiceFilter


	def get_context_data(self, *args, **kwargs):
		context = super(ServiceListView, self).get_context_data(*args, **kwargs)
		context["now"] = timezone.now()
		context["query"] = self.request.GET.get("q") #None
		context["filter_form"] = ServiceFilterForm(data=self.request.GET or None)
		return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ServiceListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
		return qs


import random
class ServiceDetailView(DetailView):
	model = Service
	#template_name = "service.html"
	#template_name = "<appname>/<modelname>_detail.html"
	def get_context_data(self, *args, **kwargs):
		context = super(ServiceDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		#order_by("-title")
		context["related"] = sorted(Service.objects.get_related(instance)[:6], key= lambda x: random.random())
		return context



from services.forms import ServiceCreateForm, ServiceUpdateForm, VariationInventoryCreateForm
from django.contrib import messages

def service_create_view(request):
	if not request.user.shopaccount_set.filter(user=request.user):
		raise Http404
	user = request.user
	shop = ShopAccount.objects.filter(user=user)
	form = ServiceCreateForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.shop = ShopAccount.objects.get(user=user)
		instance.save()

		messages.success(request, 'Service Created Successfully!')
		return HttpResponseRedirect('/add-service-variations/')

	context = {
		"form": form,
	}
	return render (request, "services/service_create.html", context)


def service_update_view(request, pk=None):
	if not request.user.shopaccount_set.filter(user=request.user):
		raise Http404
	instance = get_object_or_404(Service, id=pk)
	form = ServiceUpdateForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		return HttpResponseRedirect('/shops/')

	context = {
		"title":instance.title,
		"instance":instance,
		"form":form,
	}
	return render (request, "services/service_update.html", context)


def myservices(request, pk=None):
	if not request.user.shopaccount_set.filter(user=request.user):
		raise Http404
	if not request.user.is_authenticated():
		raise Http404
	user = request.user
	shop = ShopAccount.objects.filter(user=user)
	shop_service = Service.objects.filter(shop=shop)
	print (shop_service)
	context = {
		"service":shop_service
	}
	return render(request, "services/myservices.html", context)



def variation_create_view(request):
	if not request.user.shopaccount_set.filter(user=request.user):
		raise Http404
	form = VariationInventoryCreateForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()

		messages.success(request, 'Variations Added Successfully')
		return  HttpResponseRedirect('/shops/')
	context = {
		"form":form
	}
	return render(request, "services/variations_create.html", context)

		

def service_detail_view_func(request, id):
	#service_instance = Service.objects.get(id=id)
	service_instance = get_object_or_404(Service, id=id)
	try:
		service_instance = Service.objects.get(id=id)
	except Service.DoesNotExist:
		raise Http404
	except:
		raise Http404

	template = "services/service_detail.html"
	context = {	
		"object": service_instance
	}
	return render(request, template, context)