from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
from django.core.validators import MinLengthValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('E-mail address is mandatory')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

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
    is_activated = models.BooleanField(default=False)
    activation_token = models.CharField(
        max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.activation_token:
            self.activation_token = get_random_string(length=40)
        super().save(*args, **kwargs)

# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parents = models.ManyToManyField(
        Parent, related_name='students', blank=True)
    grade = models.CharField(max_length=10)
    birth_date = models.DateField()
    allergies = models.ManyToManyField(
        'Allergy',
        blank=True,
        verbose_name="Allergies et restrictions alimentaires"
    )

    def __str__(self):
        parent_names = ", ".join(
            [f"{parent.user.first_name} {parent.user.last_name}" for parent in self.parents.all()])
        return f"{self.user.first_name} {self.user.last_name} - {self.grade} (Parents: {parent_names})"

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


class SchoolZone(models.Model):
    """représente une zone scolaire"""
    ZONE_CHOICES = [
        ('A', 'Zone A'),
        ('B', 'Zone B'),
        ('C', 'Zone C'),
    ]

    name = models.CharField(
        max_length=1,
        choices=ZONE_CHOICES,
        unique=True,
        verbose_name="Nom de la zone"
    )

    def __str__(self):
        return self.get_name_display()


class Holidays(models.Model):
    """vacances scolaires"""
    zone = models.ForeignKey(
        SchoolZone,
        on_delete=models.CASCADE,
        related_name="holidays",
        verbose_name="Zone accadémique"
    )
    start_date = models.DateField(verbose_name="Date de début des vacances")
    end_date = models.DateField(verbose_name="Date de fin des vacances")
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Description des vacances"
    )
    school_year = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(9)],
        verbose_name="Année scolaire"
    )

    def __str__(self):
        return f"{self.description} ({self.start_date} - {self.end_date})"


class Allergy(models.Model):
    """gérer les allergies et restrictions alimentaires"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Type d'allergies ou restrictions alimentaires"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description détaillée"
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Faible'),
            ('MEDIUM', 'Moyen'),
            ('HIGH', 'Élevé'),
            ('CRITICAL', 'Critique')
        ],
        default='LOW',
        verbose_name="Niveau de sévérité"
    )

    class Meta:
        verbose_name = "Allergie"
        verbose_name_plural = "Allergies"

    def __str__(self):
        return self.name
