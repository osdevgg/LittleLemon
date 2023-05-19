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

# Unique and UniqueTogether Validators
from rest_framework.validators import UniqueValidator
from rest_framework.validators import UniqueTogetherValidator

import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
# Commented for validation Method 2, which defines 'stock' elsewhere
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
#    category = serializers.StringRelatedField()
# And for nested related can be replaced with depth in Meta class below
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
# Validation
# price > 2.00
# Validation Method 1: Conditions in the field
#    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)

# Validation Method:3 Using validate_field() method 
#    def validate_price(self, value):
#        if (value < 2):
#            raise serializers.ValidationError('Price should not be less than 2.0')
#
#    def validate_stock(self, value):
#        if (value < 0):
#            raise serializers.ValidationError('Stock cannot be negative')
        
# Validation Method 4: Using the validate() method 
    def validate(self, attrs):
# Sanitization 2 within validate function
        attrs['title'] = bleach.clean(attrs['title'])
        if(attrs['price']<2):
            raise serializers.ValidationError('Price should not be less than 2.0')
#   use the actual field name for validating the stock which is inventory.        
        if(attrs['inventory']<0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
    
# Unique Validator before class Meta
#    title = serializers.CharField(
#        max_length=255,
#        validators=[UniqueValidator(queryset=MenuItem.objects.all())]
#    )
    
# Sanitization
# 1 with validate_field
#    def validate_title(self, value):
#        return bleach.clean(value)

    class Meta:
        model = MenuItem
        fields = [ 'id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id' ]
#        depth = 1
# Validation Method 2: Using keyword arguments in the Meta class
#        extra_kwargs = {
#             'price': {'min_value': 2},
#             'stock':{'source':'inventory', 'min_value': 0}
#        }
#    
# Unique Validator in class Meta
#        extra_kwargs = {
#            'title': {
#                'validators': [
#                    UniqueValidator(
#                        queryset=MenuItem.objects.all()
#                    )
#                ]
#            }
#        } 
# 
# UniqueTogether Validator in class Meta
        validators = [
            UniqueTogetherValidator(
                    queryset=MenuItem.objects.all(),
                    fields=['title', 'price']
            ),
        ]

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)    