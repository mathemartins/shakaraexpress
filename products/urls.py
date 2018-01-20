from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from products.views import (
        ProductCreateView,
        ProductDetailView,
        ProductListView,
        ProductUpdateView,
        )

urlpatterns = [
    url(r'^$', ProductListView.as_view(), name='list'), #products:list
    url(r'^(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),
    url(r'^(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),
   

]   