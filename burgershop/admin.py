# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import admin
from .models import Item, Category
from .models import Order, OrderRow
from .models import Restaurant, Waiter

# Register your models here.

# Menu
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

class ItemInline(admin.StackedInline):
    model = Item
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [ItemInline]

# Infrastructure

class WaiterAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant')

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('address', 'city')

# Orders

class OrderRowInline(admin.StackedInline):
    model = OrderRow
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'waiter', 'datetime', 'cost', 'status_active', 'status_purchased')
    inlines = [OrderRowInline]
#    form = OrderForm


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Waiter, WaiterAdmin)
