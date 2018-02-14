from django import forms
from shops.models import ShopAccount

class NewShopForm(forms.ModelForm):
	agree = forms.BooleanField(label='Agree to Terms', widget=forms.CheckboxInput(attrs={'class':'form-control'}))
	
	class Meta:
		model = ShopAccount
		fields = [
			"business_name",
			"service",
			"category",
			"mobile_number",
			"let_client_book_online",
		]
		widgets = {
			"business_name": forms.TextInput(
				attrs= {
					"placeholder": "business name",
					"class": "form-control",
				}
			),
			"address": forms.TextInput(
					attrs={
						"placeholder": "Address Of Physical Location",
						"class": "form-control",
					}
				),
			"mobile_number": forms.TextInput(
				attrs= {
					"placeholder": "format: 07012345678",
					"class": "form-control",
				},
			)
		}

class ShopUpdateForm(forms.ModelForm):
	class Meta:
		model = ShopAccount
		fields = [
			# 'managers',
			'shop_description',
			'business_mail',
			'dashboard_banner_image_1',
			'work_image',
			'user_image',
			'let_client_book_online',
			'address',
			'map_embed',
			'cancellation_policy',
			'mobile_number'
		]