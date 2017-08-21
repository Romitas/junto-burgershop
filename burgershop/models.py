# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from json import loads

# Create your models here.

@python_2_unicode_compatible
class Category(models.Model):
    parent_category = models.ForeignKey("self", blank=True, null=True, related_name='subcategories')
    name = models.CharField(max_length=200)

    def get_name(self, full_path=False):
        """Return category name, short (default) or full path"""

        if not full_path:
            return self.name

        if not self.parent_category:
            return self.name
        else:
            return '%(parent)s/%(name)s' % {'parent': self.parent_category.get_name(full_path=True), 'name': self.name}

    def as_dict(self, json=False):
        """Return class dict representation, either basic (default) or JSON serializable"""

        parent_id = None
        if self.parent_category:
            parent_id = self.parent_category.pk if json else self.parent_category

        return {
                'id':               self.pk,
                'name':             self.name,
                'parent_category':  parent_id,
                'subcategories':    [i.as_dict(json) for i in self.category_set.all()],
                'items':            [i.as_dict(json) for i in self.item_set.all()],
                }

    def __str__(self):
        return self.get_name(full_path=True)


@python_2_unicode_compatible
class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)

    def as_dict(self, json=False):
        """Return class dict representation, either basic (default) or JSON serializable"""

        price = float(self.price) if json else self.price
        category = self.category.pk if json else self.category

        return {
                'id':       self.pk,
                'name':     self.name,
                'price':    float(self.price) if json else self.price,
                'category': self.category.pk if json else self.category,
                }

    def __str__(self):
        return '%(name)s, $%(price).02f' % {'name':self.name, 'price':self.price}

@python_2_unicode_compatible
class Restaurant(models.Model):
    city = models.CharField(max_length=20, default='Moscow') # Either 'Moscow' or 'St.Petersburg'
    address = models.CharField(max_length=300)

    def __str__(self):
        return '%(city)s, %(address)s' % {'city': self.city, 'address': self.address}

@python_2_unicode_compatible
class Waiter(models.Model):
    name = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, default=None, blank=True, null=True) # since waiters (theoretically) could transfer to other restaurants

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Order(models.Model):
    datetime = models.DateTimeField('Order time', auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    waiter = models.ForeignKey(Waiter, on_delete=models.CASCADE)

    status_active    = models.BooleanField(default=True) 
    status_purchased = models.BooleanField(default=False) 
    
    def cost(self):
#        return sum([i.item.price * i.quantity for i in self.orderrow_set.all()])
        return sum([i.cost() for i in self.orderrow_set.all()])

    def as_dict(self, json=False):
        return {
                'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S.%f%z') if json else self.datetime,
                'restaurant': self.restaurant.pk if json else self.restaurant,
                'waiter': self.waiter.pk if json else self.waiter,
                'status_active': self.status_active,
                'status_purchased': self.status_purchased,
                'order_rows': [i.as_dict(json=json) for i in self.orderrow_set.all()],
                }

    def __str__(self):
        return '%(id)d, %(restaurant)s, %(waiter)s, %(datetime)s' % {'id': self.pk, 'restaurant': self.restaurant, 'waiter': self.waiter, 'datetime': self.datetime}

@python_2_unicode_compatible
class OrderRow(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
   
#    cost = models.DecimalField(default=0.0, max_digits=6, decimal_places=2)
    
    def cost(self):
        return self.item.price * self.quantity

    def as_dict(self, json=False):
        return {
                'order': self.order.pk if json else self.order,
                'item': self.item.pk if json else self.item,
                'quantity': int(self.quantity) if json else self.quantity,
                'cost': float(self.cost()) if json else self.cost(),
                }

    def __str__(self):
        return '%s, %d' % (self.item, self.quantity)
