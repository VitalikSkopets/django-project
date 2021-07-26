from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from ecarshop.settings import EMAIL_ADMIN
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
            }
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         vehicle=item['vehicle'],
                                         price=item['price'],
                                         quantity=item['quantity']
                                         )
            cart.clear()
            messages.success(request, "Your order has been successfully completed.")
            html_body = render_to_string('orders/order/email.html', body)
            message = EmailMultiAlternatives(subject="The order was placed on the Shop E-car Website",
                                             to=[EMAIL_ADMIN, body.get('email')],
                                             )
            message.attach_alternative(html_body, "text/html")
            try:
                message.send(fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request=request, template_name='orders/order/created.html', context={'title': 'Thanks!',
                                                                                               'order': order,
                                                                                               }
                          )
    else:
        form = OrderCreateForm()
        context = {
            'title': 'Checkout',
            'cart': cart,
            'form': form,
        }
        return render(request=request, template_name='orders/order/create.html', context=context)

def orders_all(request):
    context = {
        'title': _('All orders'),
        'message': _('Hello, World!')               
    }
    return render(request=request, template_name='orders/order/all.html', context=context)
