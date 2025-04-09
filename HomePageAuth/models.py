from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField

# ✅ Custom User Manager (For Creating Users & Superusers)


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, role="student"):
        """Creates and returns a normal user"""
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)

        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        """Creates and returns a superuser"""
        user = self.create_user(
            email=email, username=username, password=password, role="admin")
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# ✅ Custom User Model (Replaces `Role` with a Simple String Field)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("student", "Student"),
        ("teacher", "Teacher"),
    ]

    email = models.EmailField(unique=True)
    # ✅ Now a simple CharField
    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="student")

    objects = UserManager()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_permissions_set", blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ✅ Profile Model (For Additional User Details)


class Profile(models.Model):
    TECHNOLOGY_CHOICES = [
        ('FOT', 'Faculty of Technology'),
        ('FMS', 'Faculty of Medical Science'),
    ]
    DEGREE_CHOICES = [
        ('B.Tech', 'B.Tech'),
        ('M.Tech', 'M.Tech'),
        ('MBBS', 'MBBS'),
    ]
    BRANCH_CHOICES = [
        ('CE', 'Computer Engineering'),
        ('EC', 'Electronics & Communication'),
        ('CH', 'Chemical Engineering'),
        ('MH', 'Mechanical Engineering'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    technology_type = models.CharField(
        max_length=20, choices=TECHNOLOGY_CHOICES)
    degree_type = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    branch = models.CharField(
        max_length=50, choices=BRANCH_CHOICES, default='CE')
    semester = models.IntegerField(default=1)

    full_name = models.CharField(max_length=255)

    # ✅ Contact number with country code
    contact_number = PhoneNumberField(region="IN", blank=True, null=True)
    father_contact = PhoneNumberField(region="IN", blank=True, null=True)
    mother_contact = PhoneNumberField(region="IN", blank=True, null=True)

    image = models.ImageField(
        upload_to="profile_pics/", default="default.jpg", blank=True, null=True)

    def __str__(self):
        return self.user.username
