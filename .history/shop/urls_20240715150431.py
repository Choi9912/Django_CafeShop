from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static

app_name = 'shop'

from django.urls import path
from . import views
"""################################
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/<int:pk>/order_list/', views.order_list, name='order_list'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('<int:category_id>/', views.show_category, name='show_category'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/cart_or_buy/', views.cart_or_buy, name='cart_or_buy'),
    path('cart/<int:pk>/', views.cart, name='cart'),
    path('cart/<int:pk>/delete/', views.delete_cart, name='delete_cart'),
]
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('order_list/<int:pk>/', views.order_list, name='order_list'),
    path('category/<int:category_id>/', views.show_category, name='show_category'),
    path('product_detail/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/<int:pk>/', views.cart, name='cart'),
    path('cart/delete/<int:pk>/', views.delete_cart, name='delete_cart'),
    path('cart_or_buy/<int:pk>/', views.cart_or_buy, name='cart_or_buy'),
]
