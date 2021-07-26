from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['vehicle']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'paid', 'created', 'updated')
    list_filter = ('city', 'paid', 'created', 'updated')
    list_editable = ('paid',)
    search_fields = ('last_name', 'email', 'phone')
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
