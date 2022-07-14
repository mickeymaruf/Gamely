from django.urls import path

from . import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/<int:order_number>/', views.payments, name="payments"),
    path('create_checkout_session/', views.create_checkout_session, name="create_checkout_session"),
    path('order_complete/', views.order_complete, name="order_complete"),
    path('cancel_order/<int:order_number>/', views.cancel_order, name="cancel_order"),

    path('create_stripe_products/', views.create_stripe_products, name="create_stripe_products"),
]