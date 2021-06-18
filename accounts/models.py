from django.shortcuts import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManger

# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    phone = models.CharField(max_length=10)
    ostan = models.CharField(max_length=50, null=True, blank=True)
    zipcode = models.CharField(max_length=10)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_shopadmin = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManger()


    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_lable):
        return True

    @property
    def is_staff(self):
        return self.is_admin            


 