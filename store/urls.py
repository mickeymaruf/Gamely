from django.urls import path

from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('category/', views.category, name="category"),
    path('category/<slug:category_slug>/', views.store, name="product_by_catory"),
    path('category/<slug:category_slug>/<str:product_slug>/', views.single_product, name="single_product"),
    
    path('submit_review/<slug:product_slug>/', views.submit_review, name="submit_review"),
    path('search/', views.search, name="search"),
]