from rest_framework import generics , response
from .serializer import ProductSerializer , CategoryListSerializer , ProductDetailSerializer
from .models import Product , Category
from django.shortcuts import get_object_or_404

# Create your views here.

#todo : fix category problem
class ProductList(generics.ListAPIView):

    """ show list products  """

    queryset = Product.active.all()
    serializer_class = ProductSerializer


class CategoryList(generics.ListAPIView):

    """ show list categories"""

    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryProductList(generics.ListAPIView):

    """ show list product of given category"""


    serializer_class = ProductSerializer
    
    def get_queryset(self):
        category = get_object_or_404(Category,pk = self.kwargs['pk'])
        product = category.pcat.filter(is_active=True,status='p',storage__gt=0)
        return product


class ProductRetrive(generics.RetrieveAPIView):

    """ show detail of product , comment of product and add comment , related product """

    queryset = Product.active.all()
    serializer_class = ProductDetailSerializer


class RelatedProduct(generics.ListAPIView):

    """ show list product that related to given pk """
    
    serializer_class = ProductSerializer

    def get_queryset(self):
        product = Product.objects.get(pk=self.kwargs['pk'])
        related_products = Product.active.filter(category__in=product.category.all()).distinct() 
        related_products = related_products.exclude(pk=product.pk) 
        return related_products