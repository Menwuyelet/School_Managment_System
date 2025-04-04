from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
# Create your models here.

## used to store multivalue contact data for each human entity
class Contact(models.Model):
    email = models.EmailField(max_length = 200, unique = True, blank = True, default = "")
    phone = models.CharField(max_length = 20, unique = True, blank = True, default = "")
    
    def __str__(self):
        return f"{self.email}, {self.phone}"
    

## used to store multivalue address data for each human entity
class Address(models.Model):
    city = models.CharField(max_length = 100, blank = False)
    kebele = models.CharField(max_length = 20, blank = False)
    home_number = models.CharField(max_length = 20, blank = True)
    postal_number = models.CharField(max_length = 20, blank = True)

    def __str__(self):
        return f"{self.city}, {self.kebele}, {self.home_number}, {self.postal_number}"


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email , phone, city, kebele, home_number, postal_number,  password,  **extra_fields):
        if not first_name or not last_name:
            raise ValueError("Users must have first and last name.")
        # Create Contact and Address objects
        contact = Contact.objects.create(email = email, phone = phone)
        address = Address.objects.create(city = city, kebele = kebele, home_number = home_number, postal_number = postal_number)
        user = self.model(first_name = first_name, last_name = last_name, contact = contact, address = address , **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, last_name, email , phone, city, kebele, home_number, postal_number, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(first_name = first_name, last_name = last_name, password = password, email = email, phone = phone, city = city, kebele = kebele, home_number = home_number, postal_number = postal_number, **extra_fields)


## this class serves as blue print for other human entities.
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key = True, max_length = 15, unique = True)
    first_name = models.CharField(max_length = 100, blank = False)
    last_name = models.CharField(max_length = 100, blank = False)
    date_of_birth = models.DateField()
    contact = models.OneToOneField(Contact, on_delete = models.CASCADE, related_name = 'contact')
    address = models.ForeignKey(Address, on_delete = models.CASCADE, related_name = 'address')
    school_abbr = models.CharField(max_length = 10, default = "SCH")

    GENDER_CHOICE =[('Male', 'Male'), ('Female','Female')]
    gender = models.CharField(max_length= 10, choices = GENDER_CHOICE)

    is_superuser = models.BooleanField(default =  False)
    is_staff = models.BooleanField(default = False)

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth',  'gender']

    objects = UserManager()

    def __str__(self):
        return f"{self.user_id} - {self.first_name} {self.last_name}"