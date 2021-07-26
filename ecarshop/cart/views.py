from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from shop.models import Vehicle
from .cart import Cart
from .forms import CartAddVehicleForm


@require_POST
def cart_add(request, vehicle_slug):
    cart = Cart(request)
    vehicle = get_object_or_404(Vehicle, slug=vehicle_slug)
    form = CartAddVehicleForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(vehicle=vehicle, quantity=cd['quantity'], update_quantity=cd['update'])
    messages.success(request, "Vehicle added to shopping cart")
    return redirect(to='cart:cart_detail')


def cart_remove(request, vehicle_slug):
    cart = Cart(request)
    vehicle = get_object_or_404(Vehicle, slug=vehicle_slug)
    cart.remove(vehicle)
    messages.success(request, "Vehicle removed from shopping cart")
    return redirect(to='cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddVehicleForm(initial={'quantity': item['quantity'],
                                                                   'update': True}
                                                          )
    context = {
        'title': 'Your Shopping Cart',
        'cart': cart,
    }
    return render(request=request, template_name='cart/detail.html', context=context)
