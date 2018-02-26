from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
from django.db.models import Q, Avg, Count
from django.http import Http404, HttpResponse, JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from dev.mixins import LoginRequiredMixin
# from products.models import Product

from shops.forms import NewShopForm, ShopUpdateForm
from shops.mixins import ShopAccountMixin
from shops.models import ShopAccount
from dev.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin, 
			SubmitBtnMixin,
			AjaxRequiredMixin
			)


class ShopProductDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, pk=kwargs['pk'])
        return obj.get_absolute_url()


# class ShopTransactionListView(ShopAccountMixin, ListView):
# 	model = Transaction
# 	template_name = "shops/transaction_list_view.html"

# 	def get_queryset(self):
# 		return self.get_transactions()


class ShopDashboard(ShopAccountMixin, FormMixin, View):
	form_class = NewShopForm
	success_url = "/shop/"

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get(self, request, *args, **kwargs):
		apply_form = self.get_form() #NewShopForm()
		account = self.get_account()
		print (account)
		exists = account
		active = None
		context = {}
		if exists:
			active = account.active
		if not exists and not active:
			context["title"] = "Apply for Account"
			context["apply_form"] = apply_form
		elif exists and not active:
			context["title"] = "Account Activation Pending"
		elif exists and active:
			context["title"] = "My Shop Dashboard"
			
			#products = Product.objects.filter(shop=account)
			# context["products"] = self.get_products()
			# transactions_today = self.get_transactions_today()
			# context["transactions_today"] = transactions_today
			# context["today_sales"] = self.get_today_sales()
			# context["total_sales"] = self.get_total_sales()
			# context["transactions"] = self.get_transactions().exclude(pk__in=transactions_today)[:5]
		else:
			pass
		
		return render(request, "shops/dashboard.html", context)

	def form_valid(self, form):
		valid_data = super(ShopDashboard, self).form_valid(form)
		business_name = form.cleaned_data['business_name']
		mobile_number = form.cleaned_data['mobile_number']
		category = form.cleaned_data['category']
		obj = ShopAccount.objects.create(
			user=self.request.user,
			business_name = business_name,
			mobile_number = mobile_number,
			category = category
		)
		return valid_data


def shop_account_update(request, slug=None):
	obj = get_object_or_404(ShopAccount, slug=slug)
	shop_form = ShopUpdateForm(request.POST or None, request.FILES or None, instance=obj)
	if shop_form.is_valid():
		instance = shop_form.save(commit=False)
		instance.save()
		return HttpResponseRedirect(obj.get_absolute_url())
		messages.success(request, "<strong>Shop Update</strong> successful ", extra_tags='html_safe')
	template = "shops/shop_update.html"
	context = {
		"object": obj,
		"shop_form": shop_form,
		"submit_btn": "Update Shop"
		}
	return render(request, template, context)



class ShopAccountDetailView(MultiSlugMixin, DetailView):
	model = ShopAccount
	template_name = "shops/shop_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ShopAccountDetailView, self).get_context_data(*args, **kwargs)
		return context


class ShopList(ListView):
	model = ShopAccount
	template_name = "shops/shop_list.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(ShopList, self).get_queryset(**kwargs)
		query = self.request.GET.get("q")
		query2 = self.request.GET.get("q2")
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
		return qs