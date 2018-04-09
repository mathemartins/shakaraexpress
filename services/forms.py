from django import forms

from django.forms.models import modelformset_factory

from .models import Variation, Category, Service, ServiceImage


CAT_CHOICES = (
	('electronics', 'Electronics'),
	('accessories', 'Accessories'),
)

class ServiceFilterForm(forms.Form):
	q = forms.CharField(label='Search', required=False)
	category_id = forms.ModelMultipleChoiceField(
		label='Category',
		queryset=Category.objects.all(), 
		widget=forms.CheckboxSelectMultiple, 
		required=False)
	# category_title = forms.ChoiceField(
	# 	label='Category',
	# 	choices=CAT_CHOICES, 
	# 	widget=forms.CheckboxSelectMultiple, 
	# 	required=False)
	max_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)
	min_price = forms.DecimalField(decimal_places=2, max_digits=12, required=False)



class VariationInventoryForm(forms.ModelForm):
	class Meta:
		model = Variation
		fields = [
			"price",
			"sale_price",
			"inventory",
			"active",
		]


VariationInventoryFormSet = modelformset_factory(Variation, form=VariationInventoryForm, extra=0)


class VariationInventoryCreateForm(forms.ModelForm):
	class Meta:
		model = Variation
		fields = [
			'title',
			'price',
			'sale_price',
			'active',
			'inventory',
		]



class ServiceCreateForm(forms.ModelForm):
	class Meta:
		model = Service
		fields = [
			"title",
			"description",
			"price",
			"category",
			"display_image",
			"default",
		]


class ServiceImageUploadForm(forms.ModelForm):
	class Meta:
		model = ServiceImage
		fields = [
			"image"
		]


class ServiceUpdateForm(forms.ModelForm):
	class Meta:
		model = Service
		fields = [
			"title",
			"description",
			"price",
			"categories",
			"default",
		]