from django.db import models
from users.models import User
from datetime import date
# Create your models here.

## serve to store the backing details of staffs 
# see if the relation causes problem in creation
class BankAccount(models.Model):
    bank_name = models.CharField(max_length = 100, blank = False)
    account_number = models.CharField(max_length = 100, blank = False)

## serves to hold all staffs in the school extending the User model
class Staff(User):
    role = models.CharField(max_length = 100, blank = False)
    hiring_date = models.DateField(default = date.today)
    salary = models.FloatField(blank = False)
    bank_account = models.OneToOneField(BankAccount, on_delete = models.CASCADE, unique = True)
    ## to generate a unique id for each staff members
    def save(self, *args, **kwargs):
        if not self.user_id:
            year_suffix = str(self.hiring_date.year)[-2:]
            last_staff = Staff.objects.filter(user_id__endswith=f"/{year_suffix}", user_id__startswith = f"{self.school_abbr}/S") \
                                      .order_by('-user_id').first()
            last_number = int(last_staff.user_id.split('/')[1][1:]) + 1 if last_staff else 1000
            self.usre_id = f"{self.school_abbr}/S{last_number}/{year_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.staff_id 