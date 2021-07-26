from cart.forms import CartAddVehicleForm


menu = [{'title': 'Gallery', 'url_name': 'shop:gallery'},
        {'title': 'Contact', 'url_name': 'shop:contact'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        context['cart_vehicle_form'] = CartAddVehicleForm
        return context
