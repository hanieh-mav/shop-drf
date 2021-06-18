from rest_framework import serializers , exceptions, validators
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model


phone_regex = RegexValidator(regex=r'^\d{10}$',message='Phone number must be entered in the format:''9137866088')


#registerserializer
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=5)
    password = serializers.CharField(min_length=8, max_length=30)
    phone = serializers.CharField(validators=[phone_regex],max_length=10)

    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','email','phone','ostan','zipcode','address']

    #check password not weak
    def validate_password(self, password):
        if not any (ch.isdigit() for ch in password):
            raise exceptions.ValidationError('Password must have numbers')
        if not any (ch.isalpha() for ch in password):
            raise exceptions.ValidationError('Password must have alphabet') 
        return password
