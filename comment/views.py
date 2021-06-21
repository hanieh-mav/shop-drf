import comment
from rest_framework import generics , response
from .serializer import CommentSerializer
from .models import Comment
from shop.models import Product
from django.shortcuts import get_object_or_404

# Create your views here.

class CommentListAdd(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        product = Product.active.get(pk=self.kwargs['pk'])
        comment = Comment.objects.filter(product=product)
        return comment

    
    def perform_create(self, serializer):
        user = self.request.user
        product = Product.active.get( pk = self.kwargs['pk'] )
        serializer.save( user = user , product = product )

