from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('<slug:category_slug>/', views.store, name="product_by_catory"),
    path('<slug:category_slug>/<str:product_name>/', views.single_product, name="single_product"),
]