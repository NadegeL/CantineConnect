import factory
from factory.fuzzy import FuzzyText
from api.models import User, Parent, Student, Administration, Address, SchoolClass
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

# Factory for the parent


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    phone_number = factory.Faker('phone_number', locale='fr_FR')
    country_code = 'FR'
    is_admin = False
    invoice_available = False
    address = factory.SubFactory(AddressFactory)
    is_activated = False
    relation = 'Mère'


# Factory for students
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    parent = factory.SubFactory(ParentFactory)
    grade = factory.Faker('word')
    birth_date = factory.Faker('date_of_birth')

# Factory for administration
class AdministrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administration

    # This will create a user with firstname, lastname, etc.
    user = factory.SubFactory(UserFactory)
    is_admin = True
    invoice_edited = factory.Faker('boolean')
    address = factory.SubFactory(AddressFactory)
    zone_id = factory.LazyAttribute(
    lambda _: fake.random_element(elements=zones))

# Factory for School Class
class SchoolClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolClass

    name = 'Test Class'
