from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

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

def category(request):
    context = {}
    return render(request, 'store/category.html', context)

def single_product(request, category_slug, product_slug):
    try:
        product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
        if request.user.is_authenticated:
            in_cart = CartItem.objects.filter(cart__user=request.user, product=product).exists()
        else:
            in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
            
        # reviews
        reviews = ReviewRating.objects.filter(status=True, product=product)
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

# Review & Ratings
def submit_review(request, product_slug):
    current_url = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user=request.user, product__slug=product_slug)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated!')
            return redirect(current_url)
        except:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.user = request.user
                data.product = Product.objects.get(slug=product_slug)
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted!')
                return redirect(current_url)

def search(request, is_keyword=False):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created').filter(Q(name__icontains=keyword) | Q(category__category__icontains=keyword))
            productsCount = products.count()
        else:
            products = None
            productsCount = 0

    context = {'products': products, 'productsCount': productsCount, 'keyword': keyword}
    return render(request, 'store/store.html', context)