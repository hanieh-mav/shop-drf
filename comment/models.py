from django.db import models
from accounts.models import User
from shop.models import Product
from django.shortcuts import reverse


# Create your models here.
class CommentManger(models.Manager):
    def reply(self):
        return self.filter(is_reply=True)


class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='ucomment')
    body = models.TextField()
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,related_name='pcomment')
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='romment')
    is_reply = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return '{}-{}'.format(self.user,self.body)

    objects = CommentManger()

