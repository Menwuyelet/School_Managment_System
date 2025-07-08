from django.db import models
from users.models import User
from datetime import date
# Create your models here.

## serve to store the backing details of staffs 
# see if the relation causes problem in creation
class BankAccount(models.Model):
    bank_name = models.CharField(max_length = 100, blank = False)
    account_number = models.CharField(max_length = 100, blank = False)

# ## serves to hold all staffs in the school extending the User model
class Staff(User):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    OFFICE_STAFF = 'office_staff'

    ROLE_CHOICES = [
        (ADMIN,'Admin'),
        (TEACHER, 'Teacher'),
        (OFFICE_STAFF, 'Office staff')
    ]

    role = models.CharField(max_length = 20, choices = ROLE_CHOICES)
    hiring_date = models.DateField(default = date.today)
    salary = models.FloatField(blank = False)
    bank_account = models.OneToOneField(BankAccount, on_delete = models.CASCADE, unique = True)

    def __str__(self):
        return self.user_id 