from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from bookings.models import Booking
from .models import Order


class LoginRequiredMixin(object):
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request,*args, **kwargs)



class BookingOrderMixin(object):
	def get_order(self, *args, **kwargs):
		booking = self.get_booking()
		if booking is None:
			return None
		new_order_id = self.request.session.get("order_id")
		if new_order_id is None:
			new_order = Order.objects.create(booking=booking)
			self.request.session["order_id"] = new_order.id
		else:
			new_order = Order.objects.get(id=new_order_id)
		return new_order

	def get_booking(self, *args, **kwargs):
		booking_id = self.request.session.get("booking_id")
		if booking_id == None:
			return None
		booking = Booking.objects.get(id=booking_id)
		if booking.items.count() <= 0:
			return None
		return booking