from django import forms
from django.utils.text import slugify
from newsletter.models import Newsletter


class NewsletterModelForm(forms.ModelForm):

	email = forms.CharField(label='', widget=forms.TextInput(attrs={"placeholder": "example@example.com", 'class':'form-control'}))

	class Meta:
		model = Newsletter
		fields = ('email',)