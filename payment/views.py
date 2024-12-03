from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from main.models import Product

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

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.cart_prods
        quantities = cart.get_quants
        total = cart.cart_total()

        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'shipping_info': request.POST, 'total': total, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'quantities': quantities, 'shipping_info': request.POST, 'total': total, 'billing_form': billing_form})
    else:
        messages.info(request, ('Access Denied.'))
        return redirect('home')
   
def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.cart_prods
        quantities = cart.get_quants
        total = cart.cart_total()

        payment_form = PaymentForm(request.POST or None)
        my_shipping = request.session.get('my_shipping')
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        shipping_info = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amout_paid = total

        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_info, amout_paid=amout_paid)
            create_order.save()

            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id

                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        items_quantity = value
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=items_quantity, price=product_price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.info(request, ('Order Placed'))
            return redirect('home')
        else:
            create_order = Order(full_name=full_name, email=email, shipping_address=shipping_info, amout_paid=amout_paid)
            create_order.save()

            
            order_id = create_order.pk

            for product in cart_products():
                product_id = product.id

                if product.is_sale:
                    product_price = product.sale_price
                else:
                    product_price = product.price

                for key, value in quantities().items():
                    if int(key) == product.id:
                        items_quantity = value
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=items_quantity, price=product_price)
                        create_order_item.save()

            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]

            messages.info(request, ('Order Placed'))
            return redirect('home')
    else:
        messages.info(request, ('Access Denied.'))
        return redirect('home')
   