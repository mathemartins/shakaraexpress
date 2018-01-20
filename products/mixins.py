from django.http import Http404

from dev.mixins import LoginRequiredMixin

from shops.mixins import ShopAccountMixin

class ProductManagerMixin(ShopAccountMixin, object):
	def get_object(self, *args, **kwargs):
		seller = self.get_account()
		obj = super(ProductManagerMixin, self).get_object(*args, **kwargs)
		try:
			obj.shop  == shop
		except:
			raise Http404

		if obj.shop == shop:
			return obj
		else:
			raise Http404