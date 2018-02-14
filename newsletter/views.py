from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, HttpResponseRedirect

# Create your views here.
from newsletter.models import Newsletter
from newsletter.forms import NewsletterModelForm


def newsletter_create(request):
	if request.method == "POST":
		form = NewsletterModelForm(request.POST)
		print (request.POST)

		if form.is_valid():
			email = form.cleaned_data['email']
			form.save()
			messages.success(request, "<strong>Email</strong> posted successfully", extra_tags='html_safe')
			return HttpResponseRedirect('/')
		else:
			messages.error(request, "<strong>Email</strong> error occurred", extra_tags='html_safe')
			print ("form is not valid")
			return HttpResponseRedirect('/')
	else:
		raise Http404
