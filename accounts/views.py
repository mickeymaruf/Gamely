from encodings import utf_8
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import unauthenticated_user

# User Activation Modules
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string

from .models import Account
from .forms import AccountForm

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
            messages.error(request, "Error while registration!!")
    else:
        form = AccountForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def signin(request, context=None):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email or Password Not Found!')

            context = {
                'email': email,
                'password': password
            }
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