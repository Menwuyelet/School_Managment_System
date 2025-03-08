from django.db import models
from users.models import User
from students.models import Student
# Create your models here.
class Parent(User):
    parent_id = models.CharField(max_length = 255, unique = True, editable = False)
    relation = models.CharField(max_length = 100)
    students = models.ManyToManyField(Student, related_name = "parents")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.parent_id
