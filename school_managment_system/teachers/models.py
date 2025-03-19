from django.db import models
from staffs.models import Staff
# Create your models here.

## used to create a teacher entity extending Staff class and the Staff class also extendin the User class
class Teacher(Staff):
    ## field of specialization of the teacher
    specialization = models.CharField(max_length = 255)
    def save(self, *args, **kwargs):
        if not self.user_id:
            year_suffix = str(self.hiring_date.year)[-2:]
            last_teacher = Teacher.objects.filter(user_id__endswith=f"/{year_suffix}", user_id__startswith = f"{self.school_abbr}/T") \
                                          .order_by('-user_id').first()
            last_number = int(last_teacher.user_id.split('/')[1][1:]) + 1 if last_teacher else 1000
            self.user_id = f"{self.school_abbr}/T{last_number}/{year_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id} - {self.first_name} {self.last_name}"
    
