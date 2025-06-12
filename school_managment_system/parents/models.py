from users.models import User
from datetime import datetime

## used to create a parent model extending User model
class Parent(User):

    def save(self, *args, **kwargs):
        if not self.user_id:
            year_suffix = str(datetime.now().year)[-2:]
            last_parent= Parent.objects.filter(user_id__endswith=f"/{year_suffix}", user_id__startswith=f"{self.school_abbr}/PA") \
                                            .order_by('-user_id').first()
            last_number = int(last_parent.user_id.split('/')[1]) + 1 if last_parent else 1000
            self.user_id = f"{self.school_abbr}/PA{last_number}/{year_suffix}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user_id}"



