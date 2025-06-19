-- done with models, now continue with the serializers
-- next views


--- id generating func.
"""
def save(self, *args, **kwargs):
    if not self.user_id:
        year_suffix = str(self.enrollment_date.year)[-2:]
        last_student = Student.objects.filter(user_id__endswith=f"/{year_suffix}", user_id__startswith=f"{self.school_abbr}/STU") \
                                        .order_by('-user_id').first()
        last_number = int(last_student.user_id.split('/')[1]) + 1 if last_student else 1000
        self.user_id = f"{self.school_abbr}/STU{last_number}/{year_suffix}"
    super().save(*args, **kwargs)
"""


///// test student and parent creation data
<!-- # student_data = { -->
<!-- # "first_name": "Alice",
# "last_name": "Smith",
# "date_of_birth": "2008-04-12",
# "gender": "Female",
# "contact": {
#     "email": "alice@example.com",
#     "phone": "0911122334"
# },
# "address": {
#     "city": "Addis Ababa",
#     "kebele": "01",
#     "home_number": "123",
#     "postal_number": "456"
# },
# "enrollment_date": "2023-09-01",
# # For new parent creation (nested)
# "parents": [
#     {
#         "first_name": "John",
#         "last_name": "Smith",
#         "date_of_birth": "1970-01-01",
#         "gender": "Male",
#         "contact": {
#             "email": "john@example.com",
#             "phone": "0911000000"
#         },
#         "address": {
#             "city": "Addis Ababa",
#             "kebele": "02",
#             "home_number": "789",
#             "postal_number": "000"
#         }
#     }
# ]
# }

# serializer = StudentSerializer(data=student_data)
# serializer.is_valid(raise_exception=True) 
# student = serializer.save() 
# print(student)
# print(student.parents.all()) 

# from students.serializers import StudentSerializer
# from parents.models import Parent
# from users.models import Contact, Address


# from users.models import User, Contact, Address
# from students.models import Student
# from parents.models import Parent

# # Delete in dependency-safe order
# Student.objects.all().delete()
# Parent.objects.all().delete()
# User.objects.all().delete()
# Contact.objects.all().delete()
# Address.objects.all().delete() -->






## update the staff model to support the role based permission
## update the teacher and the schedule to allow a teacher access their schedule  