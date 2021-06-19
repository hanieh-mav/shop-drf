from rest_framework import generics , exceptions , response ,status , views
from .serializer import RegisterSerializer
from django.contrib.auth import get_user_model

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

from .utilities import send_email_confirm


# Create your views here.


class Register(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        try:
            serialized_data = self.serializer_class(data=request.data)  
            # Return a 400 response if the data was invalid.
            if serialized_data.is_valid(raise_exception=True):
                email = serialized_data.data['email']
                phone = serialized_data.data['phone']
                user = get_user_model().objects.get(email=email)
                if user and user.email_confirmed:
                    raise exceptions.ErrorDetail('This email is registered before.',code=1)
                elif phone:
                    raise exceptions.ErrorDetail('This phone is registered before.',code=1)
                else:
                    user.is_active = False
                    user.save()
                    send_email_confirm(user,request)
                    return response.Response({'message':'check email'},status=status.HTTP_200_OK)
        except exceptions.ValidationError as error:
            return response.Response(error.detail,status=error.status_code)


class ActivateAccount(views.APIView):
    def get(self, request, uidb64, token,):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
