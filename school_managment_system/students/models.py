from django.db import models
from acadamics.models import Classes, Subject, Schedule, History
from parents.models import Parent
from teachers.models import Teacher
from users.models import User
from datetime import date
from decimal import Decimal
# Create your models here.

## used to create Student user extending the User model and adding additional relations
class Student(User):
    enrollment_date = models.DateField(default = date.today)
   
    # Relationships
    class_assigned = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='students')
    parents = models.ManyToManyField(Parent, related_name='children')
    histories = models.ManyToManyField(History, related_name='students')

    # Inheriting attributes from class (Subjects, Schedule, Teachers, Homeroom Teacher)
    subjects = models.ManyToManyField(Subject, related_name='students')
    schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, null=True, related_name='students')
    teachers = models.ManyToManyField(Teacher, related_name='students')
    homeroom_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='homeroom_students')

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
class Payment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Overdue', 'Overdue'),
    ]

    PAYMENT_METHODS = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Mobile Payment', 'Mobile Payment'),
    ]

    student = models.ForeignKey(Student, on_delete = models.CASCADE, related_name = "payments")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)  # Total tuition fee
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default = Decimal('0.00'))  # Payments made
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)  # Last payment date
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        """Auto-update payment status based on amount paid."""
        if self.amount_paid >= self.amount_due:
            self.status = "Paid"
            self.payment_date = date.today()  # Mark last payment date
        elif date.today() > self.due_date:
            self.status = "Overdue"
        else:
            self.status = "Pending"
        super().save(*args, **kwargs)

    @property
    def balance_due(self):
        """Returns the remaining balance the student needs to pay."""
        return max(Decimal('0.00'), self.amount_due - self.amount_paid)

    def __str__(self):
        return f"{self.student.user_id} - {self.status} ({self.amount_paid}/{self.amount_due})"


## done with basic model, check the authentication part