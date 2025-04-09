from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Assignment(models.Model):
    # ✅ Auto-incremented unique ID
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                                'role': 'teacher'})  # ✅ Only teachers can create

    def __str__(self):
        return f"{self.assignment_id} - {self.title}"  # ✅ Display ID + Title
