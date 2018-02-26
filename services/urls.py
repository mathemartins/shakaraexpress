from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


from services.views import ServiceDetailView, ServiceListView,VariationListView, service_list 

urlpatterns = [
    # url(r'^$', service_list, name='services'),
    url(r'^$', ServiceListView.as_view(), name='services'),
    url(r'^(?P<pk>\d+)/$', ServiceDetailView.as_view(), name='service_detail'),
    url(r'^(?P<pk>\d+)/inventory/$', VariationListView.as_view(), name='service_inventory'),
]