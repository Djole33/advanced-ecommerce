from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress
from django.contrib import messages

# Create your views here.

def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.cart_prods
    quantities = cart.get_quants
    total = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'shipping_form': shipping_form, 'total': total})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'quantities': quantities, 'shipping_form': shipping_form, 'total': total})
