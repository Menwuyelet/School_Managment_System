from django.contrib import admin
from .models import Parent
# Register your models here.
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date_of_birth', 'contact', 'address', 'gender')
    filter_fields = ('gender', 'address')
    search_fields = ('first_name', 'user_id')

admin.site.register(Parent, ParentAdmin)