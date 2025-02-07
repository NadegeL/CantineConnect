import factory
from factory.fuzzy import FuzzyText
from api.models import User, Parent, Student, Administration, Address
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

    username = factory.Faker('user_name')
    password = factory.LazyFunction(lambda: make_password('securepassword123'))
    email = FuzzyText(length=150, prefix='user.', suffix='@example.com')

# Factory for the parent
class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    phone_number = factory.Faker('phone_number', locale='en_US')
    is_admin = factory.Faker('boolean')
    invoice_available = factory.Faker('boolean')
    address = factory.SubFactory(AddressFactory)

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
