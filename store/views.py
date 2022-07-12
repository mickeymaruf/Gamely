from django.shortcuts import render, get_object_or_404

from carts.models import CartItem
from store.forms import ReviewForm
from orders.models import OrderProduct
from store.models import Category, Product, ReviewRating
from carts.views import _cart_id

# Create your views here.

def store(request, category_slug=None):
    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, stock__gt=0, is_available=True)
    else:
        products = Product.objects.filter(stock__gt=0, is_available=True)
        category = None
    
    context = {'products': products, 'category':category}
    return render(request, 'store/store.html', context)

# context processor of category_links
def category_links(request):
    category_links = Category.objects.all()
    return {'category_links': category_links}

def single_product(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        reviews = ReviewRating.objects.filter(status=True)

        form = ReviewForm()
    except Exception as e:
        raise e

    try:
        order_product = OrderProduct.objects.filter(user=request.user, product=product).exists()
    except:
        order_product = None
    
    context = {
        'product': product,
        'in_cart': in_cart,
        'form': form,
        'order_product': order_product,
        'reviews':reviews,
    }
    return render(request, 'store/single_product.html', context)