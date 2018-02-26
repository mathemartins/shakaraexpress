from django.http import HttpResponse

from carton.cart import Cart
from products.models import Product


def add(request):
    cart = Cart(request.session)
    product = Product.objects.get(id=request.GET.get('product_id'))
    cart.add(product, price=product.price)
    return HttpResponse("Added")


def show(request):
    return render(request, 'cart.html')