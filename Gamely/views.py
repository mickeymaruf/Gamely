from django.shortcuts import render

from store.models import Category, Product

# Create your views here.

def home(request):
    products = Product.objects.filter(stock__gt=0, is_available=True).order_by("-created")
    categories = Category.objects.all()
    
    context = {'products': products, 'categories': categories}
    return render(request, 'index.html', context)