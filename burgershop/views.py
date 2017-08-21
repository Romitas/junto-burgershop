# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from rest_framework import generics, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Item, Category, Order, OrderRow
from .serializers import CategorySerializer, ItemSerializer, OrderSerializer, OrderRowSerializer
from json import dumps, loads
from datetime import datetime


def login_form(request):
    """
    Basic authorization form
    """ 
    return render(request, 'burgershop/login.html', {
        'redirect_url': request.GET['next']
        })

def login_logout(request):
    """
    Log user out
    """
    logout(request)
    return HttpResponseRedirect('/')
#    return HttpResponseRedirect(reverse('burgershop:index'))

def login_validate(request):
    """
    Validate credentials, log in if correct
    """
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(request.GET['next'])
    else:
        return render(request, 'burgershop/login.html', {'error_message': 'Invalid login credentials. Please try again'})

@csrf_exempt
def menu(request):
    """
    Return a JSON menu. Requires being logged in
    UPD: Outdated, not used
    """

    category_list = Category.objects.all()
    output = dumps([i.as_dict(json=True) for i in category_list if i.parent_category == None])
    return HttpResponse(output)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Menu"""
    queryset = Category.objects.filter(parent_category=None)
    serializer_class = CategorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    """Active orders"""
    queryset = Order.objects.filter(status_active=True)
    serializer_class = OrderSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """Unordered 'All Items' list (service)"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class OrderRowViewSet(viewsets.ReadOnlyModelViewSet):
    """Unordered 'All Order rows' list (service, read-only)"""
    queryset = OrderRow.objects.all()
    serializer_class = OrderRowSerializer

