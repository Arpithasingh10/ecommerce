#from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
