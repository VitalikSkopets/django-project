from decimal import Decimal
from django.conf import settings
from shop.models import *


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, vehicle, quantity=1, update_quantity=False):
        vehicle_slug = vehicle.slug
        if vehicle_slug not in self.cart:
            self.cart[vehicle_slug] = {'quantity': 0, 'price': str(vehicle.price)}
        if update_quantity:
            self.cart[vehicle_slug]['quantity'] = quantity
        else:
            self.cart[vehicle_slug]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, vehicle):
        vehicle_slug = vehicle.slug
        if vehicle_slug in self.cart:
            del self.cart[vehicle_slug]
        self.save()

    def __iter__(self):
        vehicle_slugs = self.cart.keys()
        vehicles = Vehicle.objects.filter(slug__in=vehicle_slugs)
        cart = self.cart.copy()
        for vehicle in vehicles:
            cart[vehicle.slug]['vehicle'] = vehicle
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
