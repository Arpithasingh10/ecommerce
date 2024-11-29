from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('order/create/', views.order_create, name='order_create'),  # Adjust if your view is named differently
    path('order-history/', views.order_history, name='order_history'),
    path('profile/', views.profile, name='profile'),
    path('categories/', views.category_list, name='category_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/apply-coupon/', views.apply_coupon, name='apply_coupon'), 
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
      
]   
