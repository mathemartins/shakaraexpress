from django import forms
from django.contrib.auth import get_user_model
from pagedown.widgets import PagedownWidget
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField

from .models import UserAddress
User = get_user_model()

class GuestCheckoutForm(forms.Form):
	email = forms.EmailField()
	email2 = forms.EmailField(label='Verify Email')

	def clean_email2(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")

		if email == email2:
			user_exists = User.objects.filter(email=email).count()
			if user_exists != 0:
				raise forms.ValidationError("This User already exists. Please login instead.")
			return email2
		else:
			raise forms.ValidationError("Please confirm emails are the same")




class AddressForm(forms.Form):
	billing_address = forms.ModelChoiceField(
			queryset=UserAddress.objects.filter(type="billing"),
			widget = forms.RadioSelect,
			empty_label = None
			)
	shipping_address = forms.ModelChoiceField(
		queryset=UserAddress.objects.filter(type="shipping"),
		widget = forms.RadioSelect,
		empty_label = None,
		
		)



class UserAddressForm(forms.ModelForm):

	def __init__(self, *args, **kwargs):
		super(UserAddressForm, self).__init__(*args, **kwargs)
		self.fields['date'].widget = widgets.AdminDateWidget()
		self.fields['time'].widget = widgets.AdminTimeWidget()
		# self.fields['mydatetime'].widget = widgets.AdminSplitDateTime()

	class Meta:
		model = UserAddress
		fields = [
			'street',
			'date',
			'time',
			'name',
			'code',
			'discounts',
			'mobile_number',
			'city',
			'state',
			'zipcode',
			'type'
		]






