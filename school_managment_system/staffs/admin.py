from django.contrib import admin
from .models import Staff, BankAccount

# Register your models here.


class StaffAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'role', 'hiring_date', 'salary')
    list_filter = ('role', 'gender')
    search_fields = ('first_name', 'user_id', 'role')
    readonly_fields = ('hiring_date',)

admin.site.register(Staff, StaffAdmin)
admin.site.register(BankAccount)