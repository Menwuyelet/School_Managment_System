from django.db import models
from users.models import User
from datetime import date
# Create your models here.
class Teacher(User):
    teacher_id = models.CharField(max_length = 15, unique = True, editable = False)
    specialization = models.CharField(max_length = 255)
    hiring_date = models.DateField(default = date.today)

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            year_suffix = str(self.hiring_date.year)[-2:]
            last_teacher = Teacher.objects.filter(teacher_id__endswith=f"/{year_suffix}") \
                                          .order_by('-teacher_id').first()
            last_number = int(last_teacher.teacher_id.split('/')[1][1:]) + 1 if last_teacher else 1000
            self.teacher_id = f"{self.school_abbr}/T{last_number}/{year_suffix}"
        self.user_id = self.teacher_id  # Authentication ID
        super().save(*args, **kwargs)

    def __str__(self):
        return self.teacher_id