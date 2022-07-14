from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from carts.models import Cart, CartItem
from .decorators import unauthenticated_user
from carts.views import _cart_id
from orders.models import Order, OrderProduct

# User Activation Modules
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

from .models import Account
from .forms import AccountForm, ProfileEditForm

# Create your views here.

@unauthenticated_user
def register(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)

            # USER ACTIVATION
            to_email = email
            subject = "Please Active Your Account to Login!"
            message = render_to_string('accounts/account_verification_email.html', {
                "user": user,
                "domain" : get_current_site(request),
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token" : default_token_generator.make_token(user),
            })
            EmailMessage(
                subject,
                message,
                to=[to_email]
            ).send()
            messages.success(request, "An activation link has been sent to your email!")
            return redirect('login')
        else:
            pass
            # messages.error(request, "Error while registration!!")
    else:
        form = AccountForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def signin(request, context={}):
    next = request.GET['next'] if 'next' in request.GET else "home"

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            try:
                cart_already_exists = Cart.objects.filter(user=user).exists()

                if not cart_already_exists:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart.user = user
                    cart.save()
                else:
                    cart = Cart.objects.get(user=user)
                    cart_item = CartItem.objects.filter(cart=cart)
                    cart_item_product = [item.product for item in cart_item]
                    
                    existing_cart_item = CartItem.objects.filter(cart__cart_id=_cart_id(request))

                    # increasing quantity while logging in if the user's cartitem is already exists
                    for item in existing_cart_item:
                        if item.product in cart_item_product:
                            ex_cart_item = CartItem.objects.get(product=item.product, cart=cart)
                            ex_cart_item.quantity+=item.quantity
                            ex_cart_item.save()
                            item.delete()
                        else:
                            item.cart = cart
                            item.save()

                    # delete unassigned cart
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    cart.delete()
            except:
                pass
            
            login(request, user)
            return redirect(next)
        else:
            messages.error(request, 'Email or Password Not Found!')

            context = {
                'email': email,
                'password': password,
            }

    # append next into the context dict for the register page
    context['next'] = next

    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

def activate(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Contratulation, your account is activated!')
        return redirect('login')
    else:
        messages.success(request, 'Invalid activation link!')
        return redirect('register')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # RESET PASSWORD EMAIL
            to_email = email
            subject = "Reset your password!"
            message = render_to_string('accounts/reset_password_email.html', {
                "user": user,
                "domain" : get_current_site(request),
                "uid" : urlsafe_base64_encode(force_bytes(user.pk)),
                "token" : default_token_generator.make_token(user),
            })
            EmailMessage(
                subject,
                message,
                to=[to_email]
            ).send()
            messages.success(request, "A Rest Password link has been sent to your email!")
            return redirect('login')
        else:
            messages.error(request, "Account doesn't exist!")
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please Reset your password!")
        return redirect('reset_password')
    else:
        messages.error(request, "This link has been expired!")
        return redirect('login')

def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            if len(password) > 5:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                print(user)
                user.set_password(password)
                user.save()
                messages.success(request, "Password reset successful!")
                return redirect('login')
            else:
                messages.error(request, "Password should be at least 6 character!")
                return redirect('reset_password')
        else:
            messages.error(request, "Password doesn't match!")
            return redirect('reset_password')

    return render(request, 'accounts/reset_password.html')


# DASHBOARD FUNCTIONALITY

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard/dashboard.html')

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(is_ordered=True, user=request.user).order_by('-created')
    context = {'orders': orders}
    return render(request, 'accounts/dashboard/my_orders.html', context)

@login_required(login_url='login')
def order_details(request, order_number):
    order = Order.objects.get(is_ordered=True, user=request.user, order_number=order_number)
    order_product = OrderProduct.objects.filter(order=order, ordered=True)
    
    context = {'order': order, 'order_product': order_product}
    return render(request, 'accounts/dashboard/order_details.html', context)

@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    
    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'accounts/dashboard/edit_profile.html', {'user': user, 'form': form})

@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if new_password == confirm_password:
            if len(new_password) > 5:
                user=request.user
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    login(request, user)
                    messages.success(request, "Password changed successfully!")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Wrong current password!")
            else:
                messages.warning(request, "Password should be at least 6 characters!")
        else:
            messages.error(request, "New password doesn't match!")
            return redirect('change_password')

    return render(request, 'accounts/dashboard/change_password.html')

def delete_account(request):
    if request.method == "POST":
        password = request.POST['password']
        if request.user.check_password(password):
            user = request.user
            user.delete()
            messages.success(request, "Account deleted successfully!")
            return redirect('login')
        else:
            messages.error(request, "Wrong password!")
            return redirect('delete_account')

    return render(request, 'accounts/dashboard/delete_account.html')