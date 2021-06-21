from django.db.models import fields
import comment
from accounts import models
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user','body','product','reply','is_reply','created')
        extra_kwargs = {
            'user':{
                'read_only':True
            },
            'reply':{
                'read_only':True
            },
            'product':{
                'read_only':True
            },
            'is_reply':{
                'read_only':True
            },

        }