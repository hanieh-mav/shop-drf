from django.core.mail import message
from rest_framework import generics , exceptions , response ,status , views , permissions
from rest_framework.utils import serializer_helpers
from .serializer import RegisterSerializer , LoginWithEmail , ChangePasswordSerializer
from django.contrib.auth import get_user_model, tokens
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from .utilities import send_email_confirm
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken




# Register with email confirmation.
class Register(generics.CreateAPIView):

    """ Register and send email confirmation """

    serializer_class = RegisterSerializer
    def post(self, request):
        serialized_data = self.serializer_class(data=request.data) 

        # Return a 400 response if the data was invalid.
        if serialized_data.is_valid(raise_exception=True):
            data = serialized_data.validated_data
            user = get_user_model().objects.create_user(email=data['email'],first_name=data['first_name']
            ,last_name=data['last_name'],phone=data['phone'],zipcode=data['zipcode'],ostan=data['ostan'],address=data['address']
            ,password=data['password'])
            user.is_active = False
            user.save()
            send_email_confirm(user,request)
            return response.Response({'message':'check email'},status=status.HTTP_200_OK)


# Activae accounts if click on link on email.
class ActivateAccount(views.APIView):
    def get(self, request, uidb64, token,):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return response.Response(status=status.HTTP_201_CREATED)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)


# Login with Email and get user Token
class Login(ObtainAuthToken):
    serializer_class = LoginWithEmail

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)

        # Return a 400 response if the data was invalid.
        if serializer_data.is_valid(raise_exception=True):
            data = serializer_data.validated_data

            try:
                user = get_user_model().objects.get(email=data['email'],email_confirmed=True)
            except exceptions.ValidationError as error:
                return response.Response(message=error.detail,status=error.status_code)

            if user.check_password(data['password']):
                token, created = Token.objects.get_or_create(user=user)
            else:
                return response.Response({"message":"password not correct"},status=status.HTTP_400_BAD_REQUEST)

            return response.Response({'token':token.key},status=status.HTTP_200_OK)



# Logout
class Logout(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self,request):
        request.auth.delete()
        return response.Response({'message':"Token Revoken"},status=status.HTTP_200_OK)       


class ChangePassword(generics.CreateAPIView):

    """ Change password and create new token """

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)

        # Return a 400 response if the data was invalid.
        if serializer_data.is_valid(raise_exception=True):
            data = serializer_data.validated_data
            user = request.user

            if user.check_password(data['old_password']):
                if user.is_active:
                    user.set_password(data['new_password'])
                    user.save()
                    token =  Token.objects.get(user=user)
                    token.delete()
                    token = Token.objects.create(user=user)
                    token.save()
                    return response.Response(status=status.HTTP_200_OK)
                else:
                    raise exceptions.ValidationError("You are not active")
            else:
                raise exceptions.ValidationError('Old password is invalid')

