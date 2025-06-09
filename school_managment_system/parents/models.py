from users.models import User

## used to create a parent model extending User model
class Parent(User):
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.user_id}"



