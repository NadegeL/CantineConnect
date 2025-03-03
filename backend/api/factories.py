import factory
from datetime import date, timedelta
from factory.fuzzy import FuzzyText
from api.models import User, Parent, Student, Administration, Address, SchoolClass, Allergy, Holidays, SchoolZone
from django.contrib.auth.hashers import make_password
from faker import Faker

# Using the French locale
fake = Faker('fr_FR')

# List of possible zones
zones = ['A', 'B', 'C', 'Corse']


# Factory for the address
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address_line_1 = factory.Faker('street_address')
    address_line_2 = factory.Faker('secondary_address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')

# Factory for the user
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = factory.LazyFunction(lambda: make_password('securepassword123'))
    email = FuzzyText(length=150, prefix='user.', suffix='@example.com')
    is_staff = True

# Factory for the parent
class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    phone_number = factory.Faker('phone_number', locale='fr_FR')
    country_code = 'FR'
    invoice_available = False
    address = factory.SubFactory(AddressFactory)
    is_activated = False
    relation = None


# Factory for School Class
class SchoolClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolClass

    name = factory.Sequence(lambda n: f'Test Class {n}')



# Factory for students
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    grade = factory.SubFactory(SchoolClassFactory)
    birth_date = factory.Faker('date_of_birth')

    @factory.post_generation
    def parents(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for parent in extracted:
            self.parents.add(parent)

    @factory.post_generation
    def allergies(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for allergy in extracted:
            self.allergies.add(allergy)

# Factory for School Zone
class SchoolZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolZone

    name = factory.Iterator(['A', 'B', 'C'])


# Factory for administration
class AdministrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administration

    # This will create a user with firstname, lastname, etc.
    user = factory.SubFactory(UserFactory)
    invoice_edited = factory.Faker('boolean')
    address = factory.SubFactory(AddressFactory)
    zone = factory.SubFactory(SchoolZoneFactory)

# Factory for Allergy
class AllergyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Allergy

    name = factory.Sequence(lambda n: f'Allergie_{n}')
    severity = factory.Iterator(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
    description = factory.Faker('text', max_nb_chars=200)

# Factory for Holidays
class HolidaysFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holidays

    zone = factory.SubFactory(SchoolZoneFactory)
    start_date = factory.Faker('date_this_year')
    end_date = factory.LazyAttribute(
        lambda obj: obj.start_date + timedelta(days=14))
    description = factory.Faker('sentence')
    school_year = factory.LazyAttribute(
        lambda _: f"{date.today().year}-{date.today().year + 1}")
