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