from django.db import models
from teachers.models import Teacher
from django.apps import apps
# Create your models here

## used to create a class model to represent the classes in the school
# See if the student can directly inherit from this class or should i define the attributes individually
class Classes(models.Model):
    class_id = models.CharField(max_length = 20, unique = True, editable = False, primary_key = True)
    class_name = models.CharField(max_length = 50, unique = True)
    accademic_year = models.CharField(max_length = 10)
    subjects = models.ManyToManyField('Subject', related_name = 'classes')
    schedule = models.ForeignKey('Schedule', on_delete = models.SET_NULL, null = True, related_name = 'classes' )
    teachers = models.ManyToManyField(Teacher, related_name = 'classes')
    homeroom_teacher = models.OneToOneField(Teacher, on_delete = models.SET_NULL, null = True, related_name = 'homeroom_teacher') ## should be unique for every class 
    def save(self, *args, **kwargs):
        if not self.class_id:
            self.class_id = f"CLS{str(self.id).zfill(3)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.class_id}, {self.class_name}"
    

## used to recored subjects.
class Subject(models.Model):
    subject_id = models.CharField(max_length = 20, unique = True, primary_key = True)
    subject_name = models.CharField(max_length = 20, blank = False, null = False)
    def save(self, *args, **kwargs):
        SUBABBR = self.subject_name[:3].upper()
        if not self.subject_id:
            super().save(*args, **kwargs)
            self.subject_id = f"{SUBABBR}{str(self.id).zfill(3)}"
            self.save(update_fields=['subject_id'])

    def __str__(self):
        return self.subject_id

## used to track schedules
class Schedule(models.Model):
    details = models.TextField()  # Store schedule details

    def __str__(self):
        return f"Schedule for {self.class_assigned}"


class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'grades')
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, related_name = 'grades')
    teacher = models.ForeignKey(Teacher, on_delete = models.SET_NULL, null = True, related_name = 'assigned_grades')  # Only teacher can update
    assessment_type = models.CharField(max_length=50)  # E.g., "Exam", "Assignment", "Quiz"
    score = models.FloatField()  # Individual assessment score

    class Meta:
        unique_together = ('student', 'subject', 'assessment_type')  # One grade per assessment per subject

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        total_grade, created = TotalGrade.objects.get_or_create(student = self.student, subject = self.subject)
        total_grade.update_total()

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.assessment_type}): {self.score}"

# Model to store total grades per subject
class TotalGrade(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'total_grades')
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, related_name = 'total_grades')
    total = models.FloatField(default=0)  # Default to 0

    class Meta:
        unique_together = ('student', 'subject')  # Ensures one total per student per subject

    def update_total(self):
        """Recalculate total grade based on all assessments."""
        self.total = sum(grade.score for grade in Grade.objects.filter(student = self.student, subject = self.subject))
        self.save()

    def __str__(self):
        return f"{self.student} - {self.subject}: Total {self.total}"

class History(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'academic_history')
    academic_year = models.CharField(max_length = 10)
    overall_status = models.CharField(max_length = 20)
    summary = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"{self.student} - {self.academic_year}, {self.overall_status}"

