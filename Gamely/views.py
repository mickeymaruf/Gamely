from django.shortcuts import render

from store.models import Product

# Create your views here.

def home(request):
    products = Product.objects.filter(stock__gt=0, is_available=True)
    
    context = {'products': products}
    return render(request, 'index.html', context)