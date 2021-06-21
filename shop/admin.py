from django.contrib import admin
from .models import Product , Category


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag','storage','category_to_str','is_active')
    list_filter = ('price','created')
    prepopulated_fields = {'slug':('name',)}
    search_fields = ('name','description')
    actions = ['make_published']

    def make_published(self,request,queryset):
       row =  queryset.update(status='p')    
       self.message_user(request,f'{row} changed to publish')
    make_published.short_description = "change to publish"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','subcat','is_subcat')
    list_filter = ('name','is_subcat')
    prepopulated_fields = {'slug':('name',)}
    search_fields = ('name',)




 