from rest_framework import serializers


# Serializers a secas
# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()


# ModelSerializer &  Relationship Serializer
from .models import MenuItem
from decimal import Decimal
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#    category = serializers.StringRelatedField()
# And for nested related can be replaced with depth in Meta class below
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = [ 'id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id' ]
#        depth = 1

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)    