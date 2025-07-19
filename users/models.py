from django.db import models, transaction
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings
from django.utils.timezone import now, localtime
from os import path
from uuid import uuid4


#======================================= Needed Method ================================================

def upload_to(instance, filename):
    file_name, ext = path.splitext(filename)
    new_filename = f"{uuid4()}{ext}"
    user = instance.user
    return f"photos/{user.replace(" ", "_")}/{new_filename}"


#====================================== CustomUserManager Model =======================================

class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, password = None):
        if not email:
            raise ValueError("Email must be entered.")
        
        user = self.model(
            username = username,
            first_name = first_name.capitalize(),
            last_name = last_name.capitalize(),
            email = self.normalize_email(email)
        )
        
        user.set_password(password)
        user.user_type = "user"
        user.save(using=self._db)
        return user
    
    
    def create_superuser(self, username, first_name, last_name, email, password = None):
        user = self.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password
        )
        
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.user_type = "backend"
        user.save(using=self._db)
        return user


#====================================== CustomUser Model ==============================================

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = [("backend","BackEnd"), ("frontend","FrontEnd"), ("admin","Admin"), ("premium","Premium"), ("user","User")]
    username = models.CharField(max_length=30, unique=True, verbose_name="Username")
    first_name = models.CharField(max_length=30, verbose_name="First Name")
    last_name = models.CharField(max_length=30, verbose_name="Last Name")
    email = models.EmailField(max_length=50, unique=True, verbose_name="Email")
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default="user", verbose_name="User Type")
    is_active = models.BooleanField(default=False, verbose_name="Being Active")
    is_premium = models.BooleanField(default=False, verbose_name="Being Premium")
    is_admin = models.BooleanField(default=False, verbose_name="Being Admin")
    is_superuser = models.BooleanField(default=False, verbose_name="Being Superuser")
    joined_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Joined At")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated At")

    def __str__(self):
        return f"{self.username}"
    
    @property
    def is_staff(self):
        return self.is_admin
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        
        
#======================================================================================================