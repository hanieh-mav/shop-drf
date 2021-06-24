from django.contrib.auth.models import BaseUserManager


class UserManger(BaseUserManager):
    def create_user(self,email,first_name,last_name,phone,zipcode,ostan,address,password=None):
        if not email:
            raise ValueError('Users must have email')

        if not phone:
            raise ValueError('Users must have phone number')

        user = self.model(email = self.normalize_email(email),first_name=first_name,last_name=last_name,
        phone=phone,ostan=ostan,address=address,zipcode=zipcode)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,phone,password=None):
        user = self.model(email = self.normalize_email(email),phone = phone)
        user.set_password(password)
        user.is_admin = True  
        user.is_shopadmin = True
        user.save(using=self._db)
        return user