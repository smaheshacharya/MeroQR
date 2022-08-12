from enum import unique
from rest_framework import serializers
from .models import Category
from .models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','cat_name','slug','cat_description','cat_image')
        read_only_field = ('id','user_id')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','category_id','name','price','pro_description','pro_pic')
        read_only_field = ('id','user_id','category_id')
   
class ProductCategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('id','cat_name','slug','cat_description','products','cat_image')
        read_only_field = ('id','user_id')
   