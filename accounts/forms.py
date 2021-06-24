from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name','phone']


    def clean_password2(self):
        cd = self.changed_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Password must match')
        return cd['password2']

    def save(self , commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save() 
        return user  


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'ostan','address','email_confirmed']

    def clean_password(self):
        return self.initial['password']


   
   
