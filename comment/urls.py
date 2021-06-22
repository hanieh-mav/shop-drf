from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('<int:pk>/',views.CommentListAdd.as_view(),name='comment_list_add'),
    path('delete-comment/<int:pk>',views.CommentDelete.as_view(),name='delete_comment'),
    path('add-reply/<int:pk_post>/<int:pk_comment>/',views.ReplyAdd.as_view(),name='add_reply'),
    path('delete-reply/<int:pk>',views.ReplyDelete.as_view(),name='delete_reply')
]
