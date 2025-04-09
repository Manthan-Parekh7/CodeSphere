# from django.db import models

# # Create your models here.
# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# class CodeFile(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE)
#     file_name = models.CharField(max_length=255)
#     file = models.FileField(upload_to='code_files/')
#     file_type = models.CharField(max_length=255)
#     subject = models.CharField(max_length=255)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.file_name + " - " + self.subject


from django.conf import settings
from django.db import models
from django.conf import settings


class CodeFile(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='code_files/')
    file_type = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} - {self.subject}"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.email}"

