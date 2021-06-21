from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('<int:pk>/',views.CommentListAdd.as_view(),name='comment_list_add')
]
