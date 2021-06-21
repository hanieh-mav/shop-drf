from django.db import models
from django.utils.html import format_html


# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100,unique=True)
    subcat = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='scat')
    is_subcat = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  
    


class ProductManager(models.Manager):
    def active(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True,status='p',storage__gt=0)


class Product(models.Model):
    STATUS_CHOICES = (
        ('d','پیش نویس'),
        ('p','منتشر شده')
    )
    name = models.CharField(max_length=100 )
    slug = models.SlugField(max_length=100,unique=True)
    category = models.ManyToManyField(Category, related_name='pcat')
    photo = models.ImageField(upload_to = 'product/%Y/%M/%d')
    description = models.TextField()
    storage = models.IntegerField()
    price = models.PositiveBigIntegerField(default=0.0)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default='d')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    
    class Meta:
        ordering = ['status','-created'] 


    def __str__(self):
        return self.name


    def image_tag(self):
        return format_html("<img src='{}' width =60 height=50>".format(self.photo.url))
    image_tag.short_description = 'تصویر'    



    def category_to_str(self):
        return '-'.join([category.name for category in self.category.all()])


    @property
    def is_availble(self):
        if self.storage == 0:
            return False
        else:
            return True
        
    objects = models.Manager()
    active = ProductManager()
