from accounts import serializer
from re import I
from django.db.models import fields
from rest_framework import serializers 
from .models import Product , Category


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','slug','subcat','is_subcat')



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','slug','category','photo','description','storage','price','created')

      
