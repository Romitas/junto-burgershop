from django.contrib.auth.models import User, Group
from .models import Order, OrderRow, Restaurant, Waiter, Item, Category
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from json import loads


# Auth

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

# Menu

class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ('category', 'name', 'price')

    category = serializers.PrimaryKeyRelatedField(many=False, queryset=Category.objects.all())

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'name', 'subcategories', 'item_set')

    name = serializers.CharField(max_length=200)
    subcategories = RecursiveField(many=True)
    item_set = ItemSerializer(many=True)

# Orders

class OrderRowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderRow
        fields = ('item', 'quantity')

#    order = serializers.ReadOnlyField(source='order.datetime')
    item = serializers.PrimaryKeyRelatedField(many=False, queryset=Item.objects.all())
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Order
        fields = ('pk', 'datetime', 'restaurant', 'waiter', 'orderrow_set', 'status_active', 'status_purchased')

    restaurant = serializers.PrimaryKeyRelatedField(many=False, queryset=Restaurant.objects.all())
    waiter = serializers.PrimaryKeyRelatedField(many=False, queryset=Waiter.objects.all())
    orderrow_set = OrderRowSerializer(many=True) 

    status_active = serializers.BooleanField()
    status_purchased = serializers.BooleanField()

    def create(self, validated_data):
        """POST"""
            
        orderrows_data = validated_data['orderrow_set']
        _ = [validated_data.pop('orderrow_set')]

        order = Order.objects.create(**validated_data)

        for orderrow in orderrows_data:
            new_orderrow = OrderRow.objects.create(order=order, item=orderrow['item'], quantity=orderrow['quantity'])
            order.orderrow_set.add(new_orderrow)

        return order

    def update(self, instance, validated_data):
        """PUT"""

        orderrows_data = validated_data['orderrow_set']
        _ = [validated_data.pop('orderrow_set')]

        if orderrows_data:
            for i in instance.orderrow_set.all():
                i.delete()
            for orderrow in orderrows_data:
                new_orderrow = OrderRow.objects.create(order=instance, item=orderrow['item'], quantity=orderrow['quantity'])
                instance.orderrow_set.add(new_orderrow)

        instance.waiter = validated_data['waiter']
        instance.restaurant = validated_data['restaurant']
        instance.status_active = validated_data['status_active']
        instance.status_purchased = validated_data['status_purchased']
        instance.save()

        return instance
