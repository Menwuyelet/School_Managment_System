from django.contrib import admin
from .models import User, Contact, Address

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'first_name', 'last_name', 'date_of_birth', 'contact', 'address', 'gender')
    filter_fields = ('gender', 'address')
    search_fields = ('first_name', 'user_id')

admin.site.register(User, UserAdmin)
admin.site.register(Contact)
admin.site.register(Address)