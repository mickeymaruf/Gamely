from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from carts.models import Cart, CartItem
from orders.forms import OrderForm
from .models import Order

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
    tax = 0
    tax_percentage = 5
    for item in cart_items:
        total += (item.product.price * item.quantity)
    tax = (tax_percentage*total)/100
    grand_total = total+tax
    #### 
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = user
            data.name = user.first_name +" "+ user.last_name
            data.contact_email = user.email
            data.contact_phone = user.phone_number
            data.delivery_email = form.cleaned_data['delivery_email']
            data.delivery_phone = form.cleaned_data['delivery_phone']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generating order number
            current_date = datetime.now().strftime("%Y/%m/%d").replace("/", "")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=user, order_number=order_number, is_ordered=False)
            context = {
                'order': order,
                'cart_items':cart_items,
                'total':total, 'tax':tax,
                'grand_total':grand_total
            }
            return render(request, 'orders/payments.html', context)
    else:
        return HttpResponse('checkout')

def payments(request):
    
    return render(request, 'orders/payments.html')