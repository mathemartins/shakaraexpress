"""dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from core import views as core_views
from dashboard.views import DashboardView
from services import views
from bookings.views import BookingView, ItemCountView, CheckoutView, CheckoutFinalView, MyBookings
from newsletter.views import newsletter_create
from orders.views import (
                    AddressSelectFormView, 
                    UserAddressCreateView, 
                    OrderList, 
                    OrderDetail)

urlpatterns = [
    url(r'^admin/shakara-express/', admin.site.urls),
    url(r'^$', core_views.homepage, name='homepage'),
    url(r'^featured/$', core_views.featured_objects, name='featured'),
    url(r'^nearby/$', core_views.nearby_shops, name='nearby'),
    url(r'^wellness/$', core_views.wellness, name='wellness'),
    url(r'^fashion/$', core_views.fashion, name='fashion'),
    url(r'^beauty/$', core_views.beauty, name='beauty'),
    url(r'^spa/$', core_views.spa, name='spa'),
    url(r'^lifestyle/$', core_views.lifestyle, name='lifestyle'),
    url(r'^deals-of-the-day/$', core_views.deal_of_the_day, name='dotd'),
    url(r'^my-bookings/$', MyBookings.as_view(), name='my_bookings'),
    url(r'^accounts/', include('allauth.urls')),
    # url(r'^cart/', include('shopping.urls')),
    url(r'^client/dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^add-service/$', views.service_create_view, name='service-create'),
    url(r'^add-service-image/$', views.service_image_view, name='service-image'),
    url(r'^update-service/(?P<pk>\d+)/$', views.service_update_view, name='service-update'),
    url(r'^my-services/$', views.myservices, name='my-service'),
    url(r'^add-service-variations/$', views.variation_create_view, name='variation-create'),
    url(r'^shops/', include("shops.urls", namespace='shop')),
    url(r'^services/', include('services.urls')),
    url(r'^categories/', include('services.urls_categories')),
    url(r'^booking/$', BookingView.as_view(), name='booking'),
    url(r'^booking/count/$', ItemCountView.as_view(), name='item_count'),
    url(r'^orders/$', OrderList.as_view(), name='orders'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^tags/', include("tags.urls", namespace='tags')),
    url(r'^newsletter-create/', newsletter_create, name='newsletter-create'),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
    url(r'^about/$', TemplateView.as_view(template_name="about.html"), name="about"),
    url(r'^terms-of-service/$', TemplateView.as_view(template_name="terms.html"), name="terms"),
    url(r'^privacy-policy/$', TemplateView.as_view(template_name="privacy.html"), name="privacy"),
    url(r'^terms-of-service/bookings-and-ecomerce/$', TemplateView.as_view(template_name="tos.html"), name="tos"),
    url(r'^partner-business-terms-and-conditions/$', TemplateView.as_view(template_name="partner.html"), name="partner-terms"),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

