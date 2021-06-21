from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('',views.ProductList.as_view(),name='show_product'),
    path('category/',views.CategoryList.as_view(),name='category_list'),
    path('category/<int:pk>/',views.CategoryProductList.as_view(),name='category_product_list'),
    path('product/<int:pk>/',views.ProductRetrive.as_view(),name='product_retrive'),
    path('product-related/<int:pk>',views.RelatedProduct.as_view(),name='related_product')
]