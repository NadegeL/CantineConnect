from .imports import *


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
            raise ValueError(
                'The superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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
                # Valide un code postal entre 4 et 10 chiffres
                regex=r'^\d{4,10}$',
                message="The postal code must contain between 4 and 10 digits."
            )
        ]
    )
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}, {self.country}"

    def clean(self):
        """
        Custom validation to check field consistency.
        """
        if not self.postal_code.isdigit():
            raise ValidationError(
                {'postal_code': "The zip code must be numeric only."})

        if len(self.country) < 3:
            raise ValidationError(
                {'country': "The country name must be at least 3 characters long."})

    def save(self, *args, **kwargs):
        """
        Call `clean()` before saving data.
        """
        self.full_clean()  # Appelle clean() et d'autres validations
        super().save(*args, **kwargs)

# Parent model
class Parent(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='parent_profile')
    phone_number = PhoneNumberField()
    country_code = models.CharField(
        max_length=2, choices=[('FR', 'France'), ('CH', 'Suisse')])
    invoice_available = models.BooleanField(default=False)
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    is_activated = models.BooleanField(default=False)
    activation_token = models.CharField(
        max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# SchoolClass model
class SchoolClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Student model
class Student(models.Model):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    parents = models.ManyToManyField(
        Parent, related_name='students', blank=True)
    grade = models.ForeignKey(
        SchoolClass, on_delete=models.SET_NULL, null=True, blank=True)
    birth_date = models.DateField()
    allergies = models.ManyToManyField(
        'Allergy', blank=True, verbose_name="Allergies et restrictions alimentaires")

    def __str__(self):
        parent_names = ", ".join(
            [f"{parent.user.first_name} {parent.user.last_name}" for parent in self.parents.all()])
        return f"{self.first_name} {self.last_name} - {self.grade.name if self.grade else 'No Class'} (Parents: {parent_names})"


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
    address = models.ForeignKey('Address', on_delete=models.CASCADE)
    zone = models.ForeignKey(
        'SchoolZone', on_delete=models.CASCADE, related_name="administrations")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self.user:
            self.user.is_staff = True
            self.user.save()
        super().save(*args, **kwargs)

class Holidays(models.Model):
    """Vacances scolaires"""
    zone = models.ForeignKey(
        SchoolZone,
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
    school_year = models.CharField(
        max_length=9,
        validators=[MinLengthValidator(9)],
        verbose_name="Année scolaire"
    )

    def __str__(self):
        return f"{self.description} ({self.start_date} - {self.end_date})"


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

    class Meta:
        verbose_name = "Allergie"
        verbose_name_plural = "Allergies"

    def __str__(self):
        return self.name
