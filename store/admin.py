from django.contrib import admin
from .models import Product, Category, ReviewRating

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("category",)}
    list_display = ('category','slug')
    list_display_links = ('category', 'slug',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ReviewRating)