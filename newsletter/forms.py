from django import forms
from django.utils.text import slugify
from newsletter.models import Newsletter


class NewsletterModelForm(forms.ModelForm):
	class Meta:
		model = Newsletter
		fields = ('email',)
