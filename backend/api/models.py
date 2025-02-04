import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Spécifiez un related_name unique ici
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Spécifiez un related_name unique ici
        blank=True
    )

    def __str__(self):
        return self.username if self.username else "No username"

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    is_admin = models.BooleanField(default=False)
    invoice_available = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        # Use of associated user information (User)
        return f"{self.user.firstname} {self.user.lastname}"


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birth_date = models.DateField()
    grade = models.CharField(max_length=10)
    parent = models.ForeignKey(
        'Parent', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        """
        Retrieve the first and last name via the user
        associated with the student through the parent.
        """

        full_name = f"{self.parent.user.firstname} {self.parent.user.lastname}"
        return f"{full_name} - {self.grade}"


class Administration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_admin = models.BooleanField(default=True)  # Default Admin
    # Invoice management
    invoice_edited = models.BooleanField(default=False)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    # Geographical area ID
    zone_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
