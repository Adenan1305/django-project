"""Defines URL patterns for portfolio."""

from django.urls import path
from . import views
app_name = 'portfolio'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('bill/', views.bill, name='bill'),
    path('service/', views.service, name='service'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    path('signout/', views.signout, name='signout'),
]