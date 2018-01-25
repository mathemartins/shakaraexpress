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

from core import views
from checkout.views import CheckoutTestView, CheckoutAjaxView
from dashboard.views import DashboardView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.homepage, name='homepage'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^client/dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^test/$', CheckoutTestView.as_view(), name='test'),
    url(r'^checkout/$', CheckoutAjaxView.as_view(), name='checkout'),
    url(r'^shops/', include("shops.urls", namespace='shop')),
    url(r'^bookings/', include('bookings.urls', namespace='book')),
    url(r'^products/', include("products.urls", namespace='products')),
    url(r'^tags/', include("tags.urls", namespace='tags')),
    url(r'^notifications/', include('notifications.urls', namespace='notify')),
    url(r'^comments/', include('django_comments_xtd.urls')),
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    
