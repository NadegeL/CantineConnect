from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
import uuid
from phonenumber_field.modelfields import PhoneNumberField


# Custom user model inheriting from AbstractUser
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # Make sure the email is unique
    email = models.EmailField(unique=True, max_length=254)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

# Address template
class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"

# Parent model
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    is_admin = models.BooleanField(default=False)
    invoice_available = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parents = models.ManyToManyField(Parent, related_name='students', blank=True)
    grade = models.CharField(max_length=10)
    birth_date = models.DateField()

    def __str__(self):
        parent_names = ", ".join([f"{parent.user.first_name} {parent.user.last_name}" for parent in self.parents.all()])
        return f"{self.user.first_name} {self.user.last_name} - {self.grade} (Parents: {parent_names})"

    @classmethod
    def create_student(cls, username, password, grade, birth_date, parents=None):
        user = User.objects.create_user(username=username, password=password)
        if parents is None:
            parents = []
        student = cls(user=user, grade=grade, birth_date=birth_date)
        student.save()
        for parent in parents:
            student.parents.add(parent)
        return student

# Administration model
class Administration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=True)
    invoice_edited = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    zone_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self.user and self.user.password:
            self.user.password = make_password(self.user.password)
            self.user.save()
        super().save(*args, **kwargs)
