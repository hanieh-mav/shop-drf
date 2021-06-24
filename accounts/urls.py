from django.urls import path 
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/',views.Register.as_view(),name='register'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('login/',views.Login.as_view(),name='login'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('change-password/',views.ChangePassword.as_view(),name='change_password')
]
