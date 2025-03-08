from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from datetime import date
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, user_id, password = "PASWORD00"):
        if not user_id:
            raise ValueError("Users must have an ID")
        user = self.model(user_id = user_id)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(user_id, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key = True)
    full_name = models.CharField(max_length = 255)
    contact = models.CharField(max_length = 100, blank = True, null = True)
    school_abbr = models.CharField(max_length = 10, default = "SCH")

    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'user_id'  
    REQUIRED_FIELDS = []

    objects = UserManager() 

    class Meta:
        abstract = True
    