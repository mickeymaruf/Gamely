from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.signin, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<uid>/<token>/', views.activate, name="activate"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uid>/<token>/', views.reset_password_validate, name="reset_password_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),

    path('my_orders/', views.my_orders, name="my_orders"),
    path('order_details/<int:order_number>/', views.order_details, name="order_details"),
    path('change_profile_picture/', views.change_profile_picture, name="change_profile_picture"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('delete_account/', views.delete_account, name="delete_account"),
]