from django.http import HttpResponse
from django.shortcuts import render

from store.models import Category, Product

# Create your views here.

def home(request):
    products = Product.objects.filter(stock__gt=0, is_available=True).order_by("-created")[:12]
    categories = Category.objects.all()[:8]
    
    context = {'products': products, 'categories': categories}
    return render(request, 'index.html', context)

def category(request):
    context = {}
    return render(request, 'store/category.html', context)