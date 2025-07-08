from django.contrib import admin
from .models import Teacher
# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date_of_birth', 'contact', 'address', 'gender', 'specialization', 'home_room')
    filter_fields = ('gender', 'address', 'specialization')
    search_fields = ('first_name', 'user_id')

admin.site.register(Teacher, TeacherAdmin)
