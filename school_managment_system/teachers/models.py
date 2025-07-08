from django.db import models
from staffs.models import Staff
# Create your models here.

## used to create a teacher entity extending Staff class and the Staff class also extending the User class
class Teacher(Staff):
    ## field of specialization of the teacher
    specialization = models.CharField(max_length = 255)
    class_assigned = models.ManyToManyField('academics.Classes', related_name = 'teachers', blank = True)
    home_room = models.ForeignKey('academics.Classes', related_name = 'head_teacher', on_delete = models.SET_NULL,null = True, blank = True)
    
    def __str__(self):
        return f"{self.user_id} - {self.first_name} {self.last_name}"
    
