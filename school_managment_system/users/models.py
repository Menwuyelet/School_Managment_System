from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
# Create your models here.

## used to store multivalue contact data for each human entity
class Contact(models.Model):
    contact_id = models.CharField(primary_key = True, max_length = 15, unique = True)
    email = models.EmailField(max_length = 200, unique = True, blank = True, default = "")
    phone = models.CharField(max_length = 20, unique = True, blank = True, default = "")

    def save(self, *args, **kwargs):
        if not self.contact_id:
            last_contact = Contact.objects.order_by('-contact_id').first()
            if last_contact:
                try:
                    last_number = int(last_contact.contact_id.replace('CON', ''))
                except ValueError:
                    last_number = 999
            else:
                last_number = 999
            self.contact_id = f"CON{last_number + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}, {self.phone}"
    

## used to store multivalue address data for each human entity
class Address(models.Model):
    address_id = models.CharField(primary_key = True, max_length = 15, unique = True)
    city = models.CharField(max_length = 100, blank = False)
    kebele = models.CharField(max_length = 20, blank = False)
    home_number = models.CharField(max_length = 20, blank = True)
    postal_number = models.CharField(max_length = 20, blank = True)

    def save(self, *args, **kwargs):
        if not self.address_id:
            last_address = Address.objects.order_by('-address_id').first()
            if last_address:
                try:
                    last_number = int(last_address.address_id.replace('ADD', ''))
                except ValueError:
                    last_number = 999
            else:
                last_number = 999
            self.address_id = f"ADD{last_number + 1}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}, {self.kebele}, {self.home_number}, {self.postal_number}"


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, password, **extra_fields):
        if not first_name or not last_name:
            raise ValueError("Users must have first and last name.")
        # Create Contact and Address objects
        user = self.model(first_name = first_name, last_name = last_name, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, first_name, last_name, password,  **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        return self.create_user(first_name = first_name, last_name = last_name, password = password, **extra_fields)


## this class serves as blue print for other human entities.
class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(primary_key = True, max_length = 15, unique = True)
    first_name = models.CharField(max_length = 100, blank = False)
    last_name = models.CharField(max_length = 100, blank = False)
    date_of_birth = models.DateField(blank = False)
    contact = models.OneToOneField(Contact, on_delete = models.CASCADE, related_name = 'user', blank = True, null = True)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, related_name = 'users', blank = True, null = True)
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