from django.http import Http404
from dev.mixins import LoginRequiredMixin
from shops.mixins import ShopAccountMixin

class BookingManagerMixin(ShopAccountMixin, object):

	def get_object(self, *args, **kwargs):
		shop = self.get_account()
		obj = super(BookingManagerMixin, self).get_object(*args, **kwargs)
		try:
			obj.business_name = shop
		except:
			raise Http404

		if obj.business_name == shop:
			return obj
		else:
			raise Http404