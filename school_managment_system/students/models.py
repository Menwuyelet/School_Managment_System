from django.db import models
from users.models import User
from django.apps import apps
from datetime import date
# Create your models here.
class Student(User):
    student_id = models.CharField(max_length = 15, unique = True, editable = False)
    enrollment_date = models.DateField(default = date.today)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length = 10, choices = [('Male', 'Male'), ('Female', 'Female')])
    parent_id = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.student_id:
            year_suffix = str(self.enrollment_date.year)[-2:]
            last_student = Student.objects.filter(student_id__endswith=f"/{year_suffix}") \
                                          .order_by('-student_id').first()
            last_number = int(last_student.student_id.split('/')[1]) + 1 if last_student else 1000
            self.student_id = f"{self.school_abbr}/STU{last_number}/{year_suffix}"
        if self.parent_id:
            Parent = apps.get_model('Parents', 'Parent') 
            try:
                parent = Parent.objects.get(parent_id = self.parent_id)
                parent.students.add(self)
            except Parent.DoesNotExist:
                raise ValueError(f"Parent with ID {self.parent_id} does not exist.")
        else:
            parent_name = kwargs.get('parent_name')
            relation = kwargs.get('relation')
            contact = kwargs.get('contact')
             
            if not all([parent_name, relation, contact]):
                raise ValueError("Parent name, relation, and contact are required to create a new parent.")

            parent = Parent.objects.create(
                parent_id = f"{self.student_id}_{parent_name}",
                relation = relation,
            )

            parent.students.add(self)
        self.user_id = self.student_id
        super().save(*args, **kwargs)

        def __str__(self):
            return self.student_id
