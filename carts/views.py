from django.shortcuts import redirect, render

from .models import Cart, CartItem
from store.models import Product

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity+=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()

    return redirect('cart')

def cart(request, total=0, grand_total=0, tax=0, tax_percentage = 5):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            total += cart_item.product.price*cart_item.quantity
        # tax calculation for each products
        tax = (tax_percentage*total)/100
    except:
        cart_items=None

    grand_total = total+tax

    context = {'cart_items': cart_items, 'total': total, 'tax': tax, 'grand_total': grand_total}
    return render(request, 'store/cart.html', context)

def cart_items_quantity(request, cart_items_quantity=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        for item in cart_items:
            cart_items_quantity += item.quantity
    except:
        cart_items=None

    return {'cart_items_quantity': cart_items_quantity}

def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)
    cart_item.delete()
    return redirect('cart')

def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')