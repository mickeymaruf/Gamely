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

    path('dashboard/', views.dashboard, name="dashboard"),
]