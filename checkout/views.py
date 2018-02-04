import datetime

from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View
from django.shortcuts import render

from products.models import Product
from bookings.models import Booking

from dev.mixins import AjaxRequiredMixin
# Create your views here.

from billing.models import Transaction, TransactionBooking


class CheckoutAjaxView(AjaxRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return JsonResponse({}, status=401)
		# credit card required ** 
		
		user = request.user
		product_id = request.POST.get("product_id")
		exists = Product.objects.filter(id=product_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		try:
			product_obj = Product.object.get(id=product_id)
		except:
			product_obj = Product.objects.filter(id=product_id).first()

		#run transaction
		#assume it's succesful
		trans_obj = Transaction.objects.create(
				user = request.user,
				product = product_obj,
				price = product_obj.get_price,
			)
		data = {}
		return JsonResponse(data)


class CheckoutTestView(View):
	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			# raise Http404
			if not request.user.is_authenticated():
				data = {
					"works": False,
				}
				return JsonResponse(data, status=401)
			data = {
				"works": True,
				"time": datetime.datetime.now(),
			}
			return JsonResponse(data)
		return HttpResponse("hello there")

	def get(self, request, *args, **kwargs):
		template = "checkout/test.html"
		context = {}
		return render(request, template, context)


class CheckoutAjaxBookingView(View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			return JsonResponse({}, status=401)
		# credit card required ** 

		user = request.user
		booking_id = request.POST.get("booking_id")
		print (booking_id)
		exists = Booking.objects.filter(id=booking_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		try:
			booking_obj = Booking.object.get(id=booking_id)
		except:
			booking_obj = Booking.objects.filter(id=booking_id).first()

		if booking_obj.mode_of_payment == 'cash':
			data = {
				"message": "You are paying cash, make sure to confirm payment on arrival",
				"booking": booking_id
			}
			return JsonResponse(data)
		else:
			#run transaction
			#assume it's succesful
			trans_obj = TransactionBooking.objects.create(
					user = request.user,
					booking = booking_obj,
				)
			data = {}
			return JsonResponse(data)

class CheckoutTestBookingView(View):
	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			# raise Http404
			if not request.user.is_authenticated():
				data = {
					"works": False,
				}
				return JsonResponse(data, status=401)
			data = {
				"works": True,
				"time": datetime.datetime.now(),
			}
			return JsonResponse(data)
		return HttpResponse("hello there")

	def get(self, request, *args, **kwargs):
		template = "checkout/confirm.html"
		context = {}
		return render(request, template, context)


# def billing_confirmation(request):
# 	card = 
# 	template = "billing/confirm.html"
# 	context = {}
# 	return render(request, template, context)