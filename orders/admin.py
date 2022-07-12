from django.contrib import admin

from .models import Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('product', 'ordered', 'product_price', 'quantity')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'order_number', 'delivery_email', 'ip', 'status', 'is_ordered', 'created']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'name', 'user']
    list_per_page = 20
    inlines = [
        OrderProductInline,
    ]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)