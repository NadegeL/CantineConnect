from .imports import *
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The e-mail address is mandatory')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(
        max_length=20,
        choices=[
            ('parent', 'Parent'),
            ('school_admin', 'Administration du Site'),
            ('django_admin', 'Administrateur du TDB de Django'),
        ]
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

# Address template
class Address(models.Model):
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9]{3,10}$',
                message="The postal code must contain between 3 and 10 alphanumeric characters."
            )
        ]
    )
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"

    def clean(self):
        super().clean()
        if len(self.country) < 2:
            raise ValidationError(
                {'country': "The country name must contain at least 2 characters."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def clean_orphans(cls):
        cls.objects.filter(parent__isnull=True,
                           administration__isnull=True).delete()

# Parent model
class Parent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='parent')
    phone_number = PhoneNumberField()
    invoice_available = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, null=True)
    is_activated = models.BooleanField(default=False)
    activation_token = models.CharField(
        max_length=50, unique=True, blank=True, null=True)
    relation = models.CharField(
        max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Address.clean_orphans()


# SchoolClass model
class SchoolClass(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Allergy(models.Model):
    """Gérer les allergies et restrictions alimentaires"""
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

    def __str__(self):
        return self.name

# Student model
class Student(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    parents = models.ManyToManyField(
        'Parent', through='ParentChildRelation', related_name='student', blank=True)
    grade = models.ForeignKey(
        'SchoolClass', on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField()
    allergies = models.ManyToManyField(
        Allergy, through='StudentAllergy', blank=True, verbose_name="Allergies et restrictions alimentaires")

    def __str__(self):
        parent_names = ", ".join(
            [f"{parent.user.first_name} {parent.user.last_name}" for parent in self.parents.all()])
        return f"{self.first_name} {self.last_name} - {self.grade.name if self.grade else 'No Class'} (Parents: {parent_names})"


class ParentChildRelation(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    relation_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.parent.user.first_name} {self.parent.user.last_name} - {self.student.first_name} {self.student.last_name}"

class StudentAllergy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    allergy = models.ForeignKey(Allergy, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.allergy}"

@receiver(post_delete, sender=StudentAllergy)
def delete_allergy_if_no_associations(sender, instance, **kwargs):
    if not StudentAllergy.objects.filter(allergy=instance.allergy).exists():
        instance.allergy.delete()

class SchoolZone(models.Model):
    """Représente une zone scolaire"""
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

    def clean(self):
        if self.name not in ['A', 'B', 'C']:
            raise ValidationError(
                "Le nom de la zone doit être 'A', 'B' ou 'C'.")

# Administration model
class Administration(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_profile')
    invoice_edited = models.BooleanField(default=False)
    address = models.ForeignKey(
        'Address', on_delete=models.SET_NULL, null=True)
    zone = models.ForeignKey(
        'SchoolZone', on_delete=models.CASCADE, related_name="administrations")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self.user:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)
        Address.clean_orphans()


class Holidays(BaseModel):
    """Vacances scolaires"""
    zone = models.ForeignKey(SchoolZone,
                             on_delete=models.CASCADE,
                             related_name="holidays",
                             verbose_name="Zone académique"
                             )
    start_date = models.DateField(verbose_name="Date de début des vacances")
    end_date = models.DateField(verbose_name="Date de fin des vacances")
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Description des vacances"
    )
    school_year = models.CharField(max_length=9,
                                   validators=[
                                       MinLengthValidator(9)],
                                   verbose_name="Année scolaire"
                                   )

    def __str__(self):
        return f"{self.description} ({self.start_date} - {self.end_date})"
