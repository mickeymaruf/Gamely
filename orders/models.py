from django.db import models

from accounts.models import Account
from store.models import Product

# Create your models here.

class Order(models.Model):
    STATUS = (
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order_number = models.CharField(max_length=20)

    name = models.CharField(max_length=50)
    contact_phone = models.CharField(max_length=50)
    delivery_phone = models.CharField(max_length=50)
    contact_email = models.EmailField(max_length=200)
    delivery_email = models.EmailField(max_length=200)

    order_total = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='new')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name