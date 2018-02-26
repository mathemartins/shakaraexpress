from django.conf.urls import include, url
from django.contrib import admin

# from products.views import (
# 		ProductCreateView,
# 		ProductUpdateView,
# 		ShopProductListView
# 	)


from shops.views import (
    ShopList,
    ShopAccountDetailView,
    shop_account_update,
    ShopDashboard,
    ShopProductDetailRedirectView,
)

urlpatterns = [
    url(r'^$', ShopDashboard.as_view(), name='dashboard'),
    # url(r'^all-professionals/$', shop_list, name='all'),
    url(r'^all-professionals/detail/(?P<slug>[\w-]+)/$', ShopAccountDetailView.as_view(), name='shop-detail'),
    url(r'^all-professionals/detail/(?P<slug>[\w-]+)/edit/$', shop_account_update, name='shop-update'),
    # url(r'^all-professionals/detail/(?P<slug>[\w-]+)/bookings/$', shop_bookings, name='shop-bookings'),
    # url(r'^transactions/$', ShopTransactionListView.as_view(), name='transactions'),
    # url(r'^products/$', ShopProductListView.as_view(), name='product_list'), #sellers:product_list
    # url(r'^products/(?P<pk>\d+)/$', ShopProductDetailRedirectView.as_view()),
    # url(r'^products/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_edit'),
    # url(r'^products/add/$', ProductCreateView.as_view(), name='product_create'),
]