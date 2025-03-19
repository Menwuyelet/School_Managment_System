from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
# Create your models here.

## used to store multivalue contact data for each human entity
class Contact(models.Model):
    email = models.EmailField(max_length = 200, unique = True, blank = True)
    phone = models.CharField(max_length = 20, unique = True, blank = True)
    
    def __str__(self):
        return f"email: {self.email}, phone: {self.phone}"

## used to store multivalue address data for each human entity
class Address(models.Model):
    city = models.CharField(max_length = 100, blank = False)
    kebele = models.CharField(max_length = 20, blank = False)
    home_number = models.CharField(max_length = 20)
    postal_number = models.CharField(max_length = 20, blank = True)

    def __str__(self):
        return f"{self.city}, {self.kebele}, {self.home_number}, {self.postal_number}"


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, password = "PASWORD00", **extra_fields):
        if not first_name or not last_name:
            raise ValueError("Users must have first and last name.")
        user = self.model(first_name = first_name, last_name = last_name, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, last_name, password, **extra_fields):
        extra_fields.setdefault("is_admin", True)
        return self.create_user(first_name, last_name, password, **extra_fields)


## this class serves as blue print for other human entities.
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key = True, max_length = 15, unique = True)
    first_name = models.CharField(max_length = 100, blank = False)
    last_name = models.CharField(max_length = 100, blank = False)
    date_of_birth = models.DateField()
    contact = models.OneToOneField(Contact, on_delete = models.CASCADE, related_name = 'teacher_contact')
    address = models.OneToOneField(Address, on_delete = models.CASCADE, related_name = 'teacher_address')
    school_abbr = models.CharField(max_length = 10, default = "SCH")

    GENDER_CHOICE =[('Male', 'Male'), ('Female','Female')]
    gender = models.CharField(choices = GENDER_CHOICE)

    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)

    USERNAME_FIELD = 'user_id'  
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'date_of_birth', 'contact', 'address']

    objects = UserManager() 

    class Meta:
        abstract = True
