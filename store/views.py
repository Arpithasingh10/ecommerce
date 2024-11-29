# Create your views here.
#from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Order, OrderItem ,Cart
from cart.cart import Cart
from .forms import OrderCreateForm
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from .models import CartItem
from store.models import Order, OrderItem



stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    cart = Cart(request)
    
    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cart': cart
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})

def order_history(request):
    # Fetch the orders related to the current logged-in user
    orders = Order.objects.filter(user=request.user)  # Assuming there's a 'user' field
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Create Stripe payment intent
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(cart.get_total_price() * 100),
                    currency='usd',
                    metadata={'order_id': order.id}
                )
                
                # Create order items
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                
                # Clear the cart
                cart.clear()
                
                return render(request, 'orders/payment.html', {
                    'client_secret': payment_intent.client_secret,
                    'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
                })
                
            except stripe.error.StripeError as e:
                messages.error(request, 'Payment error occurred. Please try again.')
                order.delete()
                return redirect('cart_detail')
    else:
        form = OrderCreateForm()
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form
    })


@login_required  # Ensures only authenticated users can access the profile
def profile(request):
    return render(request, 'templates/store/profile.html') 

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    return render(request, 'store/category_detail.html', {'category': category})

def checkout(request):
    # Your checkout logic here
    return render(request, 'store/checkout.html')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('product_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")  # Add logout message
    return redirect('product_list')  # Redirect to home page after logout

def sign_up(request):
    if request.method == "POST":  # When the user submits the form
        form = SignUpForm(request.POST)  # Take the form data
        if form.is_valid():  # If the form is correct
            user = form.save()  # Save the user
            login(request, user)  # Log the user in automatically
            messages.success(request, "You have successfully registered and are now logged in!")
            return redirect('product_list')  # Go to the product page after signing up
        else:
            messages.error(request, "There was an error in your registration. Please try again.")
    else:
        form = SignUpForm()  # If it’s the first time, show the empty form

    return render(request, 'store/sign_up.html', {'form': form})

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Default to 1 if no quantity is provided
    cart = Cart(request)  # Create or retrieve the current cart

    # Add the product to the cart (assuming your Cart class has an add method)
    cart.add(product=product, quantity=quantity)

    return redirect('cart_detail') 

def cart_view(request):
    cart = Cart(request)  # Retrieve the current cart
    cart_items = list(cart)  # Get all items in the cart
    cart_total = cart.get_total_price()  # Calculate total price if you have this method

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
    })


from django.http import HttpResponse
def cart_update(request):
    if request.method == 'POST':
        # Add your cart update logic here
        return redirect('cart')  # Redirect to the cart page after updating
    return HttpResponse("Invalid request method", status=400)

def cart_remove(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')  # Get the product ID from the POST request
        # Add logic to remove the product from the cart
        # Example:
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
        return redirect('cart')  # Redirect back to the cart page after removal
    return HttpResponse("Invalid request method", status=400)

def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        # Logic to validate and apply the coupon code
        # Example:
        valid_coupons = {'SAVE10': 10, 'SAVE20': 20}  # Example coupon codes and discounts
        if coupon_code in valid_coupons:
           request.session['discount'] = valid_coupons[coupon_code]
        else:
          request.session['coupon_error'] = 'Invalid coupon code'
        return redirect('cart')  # Redirect back to the cart page after applying the coupon
    return HttpResponse("Invalid request method", status=400)

# def checkout(request):
#     # Retrieve the user's cart items
#     try:
#         cart = Cart.objects.get(user=request.user)
#         cart_items = CartItem.objects.filter(cart=cart)
#     except Cart.DoesNotExist:
#         return redirect('cart')  # Redirect to cart if no cart exists

#     # Ensure there are items in the cart
#     if not cart_items.exists():
#         return redirect('cart')

#     # Calculate the total price
#     total_price = sum(item.product.price * item.quantity for item in cart_items)

#     if request.method == "POST":
#         # Create an order
#         order = Order.objects.create(
#             user=request.user,
#             total_price=total_price,
#             status="Pending"
#         )
#         # Link items from the cart to the order
#         for item in cart_items:
#             order.items.create(
#                 product=item.product,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )
#         # Clear the cart after the order is placed
#         cart_items.delete()
#         # Redirect to payment
#         return redirect('payment', order_id=order.id)

#     # Render the checkout page
#     return render(request, 'store/checkout.html', {
#         'cart_items': cart_items,
#         'total_price': total_price
#     })

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def payment(request, order_id):
    # Fetch the order
    try:
        order = Order.objects.get(id=order_id, user=request.user, status="Pending")
    except Order.DoesNotExist:
        return redirect('cart')

    if request.method == "POST":
        try:
            # Create a Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100),  # Amount in cents
                currency="usd",
                payment_method=request.POST['payment_method_id'],
                confirm=True,
            )
            # Update order status
            order.status = "Paid"
            order.payment_id = intent.id
            order.save()

            return redirect('order_success', order_id=order.id)
        except stripe.error.CardError as e:
            return render(request, 'store/payment.html', {'error': str(e)})

    return render(request, 'store/payment.html', {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

@login_required
def order_success(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return redirect('cart')   

    return render(request, 'store/order_success.html', {'order': order})        # cart.py
from decimal import Decimal
from django.conf import settings
from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()       
