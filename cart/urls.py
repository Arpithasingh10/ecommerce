from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # Add this if you have a cart detail view
    # Add more URLs related to cart, if needed
]
