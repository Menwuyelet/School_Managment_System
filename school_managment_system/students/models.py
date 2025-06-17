from django.db import models
from parents.models import Parent
from users.models import User
from datetime import date

# ## used to create Student user extending the User model and adding additional relations
class Student(User):
    enrollment_date = models.DateField(default = date.today)
   
    # Relationships
    class_assigned = models.ForeignKey('academics.Classes', on_delete = models.CASCADE, related_name = 'students', blank = True,  null = True)
    parents = models.ManyToManyField(Parent, related_name = 'children')

    def save(self, *args, **kwargs):
        if not self.user_id:
            year_suffix = str(self.enrollment_date.year)[-2:]
            last_student = Student.objects.filter(user_id__endswith=f"/{year_suffix}", user_id__startswith=f"{self.school_abbr}/STU") \
                                            .order_by('-user_id').first()
            last_number = int(last_student.user_id.split('/')[1]) + 1 if last_student else 1000
            self.user_id = f"{self.school_abbr}/STU{last_number}/{year_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id} - {self.first_name} {self.last_name}"
    

class StudentPayment(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'payments')
    name = models.CharField(max_length = 100, blank = False, default = 'tuition')
    description = models.CharField(max_length = 200, default = name)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    payment_date = models.DateField(default = date.today)

    PAYMENT_METHOD_CHOICE =[('Cash', 'Cash'), ('Transfer','Transfer')]
    payment_method = models.CharField(max_length= 10, choices = PAYMENT_METHOD_CHOICE, default = 'Transfer')

    payment_code = models.CharField(max_length = 30, unique = True, editable = False, default = f"{student} - {name} - {payment_date}")

    def save(self, *args, **kwargs):
        if not self.payment_code:
            self.payment_code = self.generate_payment_code()
        super().save(*args, **kwargs)

    def generate_payment_code(self):
        return f"{self.student.user_id}-{self.payment_date.strftime('%Y%m%d')}-{self.name.upper()}"

    def __str__(self):
        return f"{self.payment_code} - {self.student} - {self.name} - {self.amount}"

# ## done with basic model, check the authentication part