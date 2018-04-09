import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

# Create your views here.

from orders.forms import GuestCheckoutForm
from orders.mixins import BookingOrderMixin
from orders.models import UserCheckout, Order, UserAddress

from services.models import Variation


from .models import Booking, BookingItem




if settings.DEBUG:
	braintree.Configuration.configure(braintree.Environment.Sandbox,
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC,
      private_key=settings.BRAINTREE_PRIVATE)




class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			booking_id = self.request.session.get("booking_id")
			print (booking_id)
			if booking_id == None:
				count = 0
			else:
				booking = Booking.objects.get(id=booking_id)
				count = booking.items.count()
				print (booking)
				print (count)
			request.session["booking_item_count"] = count
			return JsonResponse({"count": count})
		else:
			print ("Happened here")
			raise Http404

class MyBookings(View):
	def get(self, request, *args, **kwargs):
		context = {}
		template = "bookings/mybookings.html"
		return render(request, template, context)

class BookingView(SingleObjectMixin, View):
	model = Booking
	template_name = "bookings/view.html"

	def get_object(self, *args, **kwargs):
		self.request.session.set_expiry(0) #5 minutes
		booking_id = self.request.session.get("booking_id")
		print(booking_id)
		if booking_id == None:
			booking = Booking()
			booking.tax_percentage = 0.050
			booking.save()
			booking_id = booking.id
			self.request.session["booking_id"] = booking_id

		booking = Booking.objects.get(id=booking_id)
		if self.request.user.is_authenticated():
			booking.user = self.request.user
			booking.save()
		return booking

	def get(self, request, *args, **kwargs):
		booking = self.get_object()
		print(booking)
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		flash_message = ""
		item_added = False
		if item_id:
			item_instance = get_object_or_404(Variation, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			booking_item, created = BookingItem.objects.get_or_create(booking=booking, item=item_instance)
			if created:
				flash_message = "Successfully added to the booking"
				item_added = True
			if delete_item:
				flash_message = "Item removed successfully."
				booking_item.delete()
			else:
				if not created:
					flash_message = "Quantity has been updated successfully."
				booking_item.quantity = qty
				booking_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("booking"))
				#return booking_item.booking.get_absolute_url()
		
		if request.is_ajax():
			try:
				total = booking_item.line_item_total
			except:
				total = None
			try:
				subtotal = booking_item.booking.subtotal
			except:
				subtotal = None

			try:
				booking_total = booking_item.booking.total
			except:
				booking_total = None

			try:
				tax_total = booking_item.booking.tax_total
			except:
				tax_total = None

			try:
				total_items = booking_item.booking.items.count()
			except:
				total_items = 0

			data = {
					"deleted": delete_item, 
					"item_added": item_added,
					"line_total": total,
					"subtotal": subtotal,
					"booking_total": booking_total,
					"tax_total": tax_total,
					"flash_message": flash_message,
					"total_items": total_items
					}

			return JsonResponse(data) 


		context = {
			"object": self.get_object()
		}
		template = self.template_name
		return render(request, template, context)




class CheckoutView(BookingOrderMixin, FormMixin, DetailView):
	model = Booking
	template_name = "bookings/checkout_view.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		booking = self.get_booking()
		if booking == None:
			return None
		return booking

	def get_context_data(self, *args, **kwargs):
		context = super(CheckoutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_check_id = self.request.session.get("user_checkout_id")
		if self.request.user.is_authenticated():
			user_can_continue = True
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()
			self.request.session["user_checkout_id"] = user_checkout.id
		elif not self.request.user.is_authenticated() and user_check_id == None:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		else:
			pass

		if user_check_id != None:
			user_can_continue = True
			if not self.request.user.is_authenticated(): #GUEST USER
				user_checkout_2 = UserCheckout.objects.get(id=user_check_id)
				context["client_token"] = user_checkout_2.get_client_token()
		
		#if self.get_booking() is not None:
		context["order"] = self.get_order()
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse("checkout")


	def get(self, request, *args, **kwargs):
		get_data = super(CheckoutView, self).get(request, *args, **kwargs)
		booking = self.get_object()
		if booking == None:
			return redirect("booking")
		new_order = self.get_order()
		user_checkout_id = request.session.get("user_checkout_id")
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			if new_order.billing_address == None or new_order.shipping_address == None:
			 	return redirect("order_address")
			new_order.user = user_checkout
			new_order.save()
		return get_data






class CheckoutFinalView(BookingOrderMixin, View):
	def post(self, request, *args, **kwargs):
		order = self.get_order()
		order_total = order.order_total
		nonce = request.POST.get("payment_method_nonce")
		if nonce:
			result = braintree.Transaction.sale({
			    "amount": order_total,
			    "payment_method_nonce": nonce,
			    "billing": {
				    "postal_code": "%s" %(order.billing_address.zipcode),
				    
				 },
			    "options": {
			        "submit_for_settlement": True
			    }
			})
			if result.is_success:
				#result.transaction.id to order
				order.mark_completed(order_id=result.transaction.id)
				messages.success(request, "Thank you for your order.")
				del request.session["booking_id"]
				del request.session["order_id"]
			else:
				#messages.success(request, "There was a problem with your order.")
				messages.success(request, "%s" %(result.message))
				return redirect("checkout")

		return redirect("order_detail", pk=order.pk)

	def get(self, request, *args, **kwargs):
		return redirect("checkout")


















