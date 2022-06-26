from django.urls import reverse
from django.db import models
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/products')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def single_product_url(self):
        return reverse('single_product', args=[self.category.slug, self.name])

class Category(models.Model):
    category = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/category-images')
    class Meta:
        verbose_name = "Category"
        verbose_name_plural  = "Categories"

    def __str__(self):
        return self.category
    
    def url(self):
        return reverse('product_by_catory', args=[self.slug])