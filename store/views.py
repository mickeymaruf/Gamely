from django.shortcuts import render, get_object_or_404
from carts.models import Cart, CartItem

from store.models import Category, Product
from carts.views import _cart_id

# Create your views here.

def store(request, category_slug=None):
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, stock__gt=0, is_available=True)
    else:
        products = Product.objects.filter(stock__gt=0, is_available=True)
    
    context = {'products': products}
    return render(request, 'store/store.html', context)

# context processor of category_links
def category_links(request):
    category_links = Category.objects.all()
    return {'category_links': category_links}

def single_product(request, category_slug, product_name):
    try:
        product = Product.objects.get(category__slug=category_slug, name=product_name)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
    except Exception as e:
        raise e
    
    context = {'product': product, 'in_cart': in_cart}
    return render(request, 'store/single_product.html', context)