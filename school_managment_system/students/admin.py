from django.contrib import admin
from .models import Student, StudentPayment
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'enrollment_date', 'date_of_birth', 'contact', 'address', 'gender', 'class_assigned')
    filter_fields = ('gender', 'address', 'class_assigned', 'parents')
    search_fields = ('first_name', 'user_id')

admin.site.register(Student, StudentAdmin)
admin.site.register(StudentPayment)
