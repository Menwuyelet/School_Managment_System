from django.db import models
from students.models import Student
from datetime import date
# Create your models here.
class History(models.Model):
    student_id = models.OneToOneField(Student, related_name = 'student')
    year = models.DateField(default = date.year)
    class_room = models.ForeignKey()
    ## continue working on the academics and other entities relations