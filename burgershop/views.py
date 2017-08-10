# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from .models import Item, Category
from json import dumps

# Create your views here.

def index(request):
    return HttpResponse("Hello, world! Here'll be a burgershop soon!")

#def get_category_contents(Category target):
#    subcategories = target.category_set()
#    items = target.items_set()
#
#    return serializers.serialize('json', items)


def menu(request):
#    items_list = Item.objects.all() 
    category_list = Category.objects.all() 
#    output = '\n'.join([i.__str__()+';' for i in items_list])
    output = dumps([i.as_dict(json=True) for i in category_list if i.parent_category == None])
    return HttpResponse(output)
