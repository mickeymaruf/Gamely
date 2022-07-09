from django.urls import path

from . import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payments/', views.payments, name="payments"),
    path('create_checkout_session/', views.create_checkout_session, name="create_checkout_session"),
]