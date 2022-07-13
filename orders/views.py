from datetime import datetime
from logging import raiseExceptions
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings

from carts.models import CartItem
from orders.forms import OrderForm
from .models import Order, OrderProduct
from store.models import Product

# Send Email
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

import stripe

stripe.api_key = settings.STRIPE_PRIVATE_KEY

# Create your views here.

@login_required(login_url='login')
def place_order(request):
    user = request.user

    # checking if there is any cart item in the cart, if it's not then redirecting user to the store page
    cart_items = CartItem.objects.filter(cart__user=user)
    cart_items_count = cart_items.count()

    if cart_items_count < 1:
        return redirect('store')

    ####
    total = 0
    for item in cart_items:
        total += (item.product.price * item.quantity)
    ####

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = user
            data.name = user.first_name + " " + user.last_name
            data.contact_email = user.email
            data.contact_phone = user.phone_number
            data.delivery_email = form.cleaned_data['delivery_email']
            data.delivery_phone = form.cleaned_data['delivery_phone']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generating order number
            current_date = datetime.now().strftime("%Y/%m/%d").replace("/", "")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(
                user=user, order_number=order_number, is_ordered=False)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
            }
            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')


@login_required(login_url='login')
def payments(request, order_number):
    # Move the cart_item to order_product table
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Getting order by user & order number cz a user can have multiple order
    order = Order.objects.get(user=request.user, order_number=order_number)

    for item in cart_items:
        order_product = OrderProduct()
        order_product.order = order
        order_product.user = request.user
        order_product.product = item.product
        order_product.quantity = item.quantity
        order_product.product_price = item.product.price
        order_product.ordered = True
        order_product.save()

        order.is_ordered = True
        order.status = 'accepted'
        order.save()

        # Reduce the quantity of the sold products
        product = Product.objects.get(name=item.product)
        product.stock -= order_product.quantity
        product.save()

    # Clear cart_items
    cart_items.delete()

    # Send order recieved email to customer
    subject = "Thank your for your order!"
    message = render_to_string('orders/order_recieved_email.html', {
        "user": request.user,
        "order": order,
    })
    EmailMessage(
        subject,
        message,
        to=[request.user.email]
    ).send()

    order_product = OrderProduct.objects.filter(order=order)

    # total
    total = 0
    for item in order_product:
        total += (item.product.price * item.quantity)

    context = {'order': order, 'order_products': order_product, 'total': total}
    return render(request, 'orders/order_complete.html', context)


@login_required(login_url='login')
def create_checkout_session(request):
    YOUR_DOMAIN = get_current_site(request).domain
    if request.method == "POST":
        order_number = request.POST['order']

    cart_items = CartItem.objects.filter(cart__user=request.user)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{'price': item.product.price_id,
                         'quantity': item.quantity, } for item in cart_items],
            mode='payment',
            success_url=f'http://{YOUR_DOMAIN}/orders/payments/{order_number}/',
            cancel_url=f'http://{YOUR_DOMAIN}/',
        )
    except:
        pass

    return redirect(checkout_session.url, code=303)

@login_required(login_url='login')
def create_stripe_products(request):
    products = Product.objects.filter(name="MLB The Show 22")
    for product in products:
        stripe_prod = stripe.Product.create(name=product)
        stripe_price = stripe.Price.create(
            unit_amount=product.price * 100,
            currency="usd",
            product=stripe_prod.stripe_id,
        )
        prod = Product.objects.get(name=product)
        prod.price_id = stripe_price.stripe_id
        prod.save()
        
    return HttpResponse('product created successfully!')

@login_required(login_url='login')
def order_complete(request):
    return render(request, 'orders/order_complete.html')