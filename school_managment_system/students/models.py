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
    
## used to track students payment status
class PaymentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Tuition", "Trip", "Library Fee"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class StudentPayment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='payments')
    category = models.ForeignKey(PaymentCategory, on_delete=models.PROTECT, related_name='payments')
    
    # Optional custom name, e.g. "Tuition March 2025" or "Trip to Museum"
    custom_name = models.CharField(max_length=100, blank=True, null=True)
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(default=date.today)
    reference_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.custom_name or self.category.name} - {self.amount}"

# ## done with basic model, check the authentication part