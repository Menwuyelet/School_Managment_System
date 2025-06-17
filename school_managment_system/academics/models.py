from django.db import models
from teachers.models import Teacher
# Create your models here



# ## used to record subjects.
class Subject(models.Model):
    subject_id = models.CharField(max_length = 20, unique = True, primary_key = True)
    subject_name = models.CharField(max_length = 20, blank = False, null = False)
    teachers = models.ManyToManyField('teachers.Teacher', related_name = 'subjects', blank = True, default = 'No Teachers' )
    def __str__(self):
        return self.subject_id

# ## used to track schedules
class Schedule(models.Model):
    schedule_id = models.CharField(max_length = 20, unique = True, primary_key = True)
    details = models.TextField()  # Store schedule details

    def __str__(self):
        return f"Schedule for {self.class_for}"

# ## used to create a class model to represent the classes in the school
# # See if the student can directly inherit from this class or should i define the attributes individually
class Classes(models.Model):
    class_id = models.CharField(max_length = 20, unique = True, primary_key = True)
    class_name = models.CharField(max_length = 50, null = False)
    academic_year = models.CharField(max_length = 10, null = False)
    subjects = models.ManyToManyField('Subject', related_name = 'classes_given_in', blank = True, default = 'No subjects')
    schedule = models.ForeignKey('Schedule', on_delete = models.SET_DEFAULT, related_name = 'class_for', default = 'No schedule')

    def __str__(self):
        return f"{self.class_id}, {self.class_name}"
    

class Grade(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'grades')
    subject = models.ForeignKey(Subject, on_delete = models.CASCADE, related_name = 'subjects')
    teacher = models.ForeignKey(Teacher, on_delete = models.SET_NULL, null = True, related_name = 'teacher')  # Only teacher can update
    assessment_type = models.CharField(max_length=50)  # E.g., "Exam", "Assignment", "Quiz"
    score = models.FloatField()  # Individual assessment score
    grade_id = models.CharField(max_length = 30, unique = True, default = f"{student} - {subject} - {assessment_type}")
    # class Meta:
    #     unique_together = ('student', 'subject', 'assessment_type')  # One grade per assessment per subject
    def __str__(self):
        return f"{self.student} - {self.subject} ({self.assessment_type}): {self.score}"
    
class History(models.Model):
    student = models.ForeignKey('students.Student', on_delete = models.CASCADE, related_name = 'academic_history')
    academic_year = models.CharField(max_length = 10)

    summary = models.TextField(blank = True, null = True)

    OVERALL_CHOICE = [('Pass', 'Pass'), ('Fail', 'Fail'), ('Incomplete', 'Incomplete')]
    overall_status = models.CharField(max_length = 10, choices = OVERALL_CHOICE)

    def __str__(self):
        return f"{self.student} - {self.academic_year}, {self.overall_status}"

