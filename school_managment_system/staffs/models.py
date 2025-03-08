from django.db import models
from users.models import User
from datetime import date
# Create your models here.
class Staff(User):
    staff_id = models.CharField(max_length = 15, unique = True, editable = False)
    role = models.CharField(max_length = 255)
    hiring_date = models.DateField(default = date.today)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            year_suffix = str(self.hiring_date.year)[-2:]
            last_staff = Staff.objects.filter(staff_id__endswith=f"/{year_suffix}") \
                                      .order_by('-staff_id').first()
            last_number = int(last_staff.staff_id.split('/')[1][1:]) + 1 if last_staff else 1000
            self.staff_id = f"{self.school_abbr}/S{last_number}/{year_suffix}"
        self.user_id = self.staff_id  # Authentication ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.staff_id 