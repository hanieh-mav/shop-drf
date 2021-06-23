import comment
from rest_framework import generics , permissions , response , status ,exceptions
from .serializer import CommentSerializer
from .models import Comment
from shop.models import Product
from django.shortcuts import get_object_or_404
from .permission import IsAuthorOrReadOnly


class CommentListAdd(generics.ListCreateAPIView):

    """ show list of product comment , add comment if authenticated """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product = Product.active.get(pk=self.kwargs['pk'])
        comment = Comment.objects.filter(product=product)
        return comment

    
    def perform_create(self, serializer):
        user = self.request.user
        product = Product.active.get( pk = self.kwargs['pk'] )
        serializer.save( user = user , product = product )


class CommentDelete(generics.RetrieveDestroyAPIView):

    """ Delete comment of product only user of that comment can delete , and shopadmin and superuser can too """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]


class ReplyAdd(generics.CreateAPIView):

    """ add reply to comment """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self,serializer):
        user = self.request.user
        product = get_object_or_404( Product , pk = self.kwargs['pk_post'] )
        comment = get_object_or_404 ( Comment , pk = self.kwargs['pk_comment'] )
        serializer.save( user = user , product = product , reply = comment , is_reply = True)
        

class ReplyDelete(generics.RetrieveDestroyAPIView):

    """ Delete reply  only user of that reply can delete , and shopadmin and superuser can too """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAuthorOrReadOnly]






