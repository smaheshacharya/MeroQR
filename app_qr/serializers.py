from enum import unique
from rest_framework import serializers
from .models import Category
from .models import Product
from .models import Resturant


class ResturantSirializer(serializers.ModelSerializer):
    class Meta:
        model = Resturant
        fields = ('id','name','slug','sub_title','timing', 'phone_number','description','logo','cover_image')
        read_only_field = ('id','user_id')

class QrSirializer(serializers.ModelSerializer):
    class Meta:
        model = Resturant
        fields = ('link','slug','qr_image','pro_pic','resturant')
        read_only_field = ('id','resturant','user_id')
   


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


   