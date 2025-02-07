import factory
from factory.fuzzy import FuzzyText
from api.models import User, Parent, Student, Administration, Address
from django.contrib.auth.hashers import make_password

# Factory pour l'adresse
class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address_line_1 = factory.Faker('street_address')
    address_line_2 = factory.Faker('secondary_address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')

# Factory pour l'utilisateur
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.LazyFunction(lambda: make_password('securepassword123'))
    email = FuzzyText(length=150, prefix='user.', suffix='@example.com')

# Factory pour le parent
class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    phone_number = factory.Faker('phone_number', locale='en_US')
    is_admin = factory.Faker('boolean')
    invoice_available = factory.Faker('boolean')
    address = factory.SubFactory(AddressFactory)

# Factory pour l'étudiant
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    parent = factory.SubFactory(ParentFactory)
    grade = factory.Faker('word')
    birth_date = factory.Faker('date_of_birth')

# Factory pour l'administration
class AdministrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administration

    user = factory.SubFactory(UserFactory)
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    password = factory.LazyFunction(lambda: make_password('securepassword123'))
    is_admin = True
    invoice_edited = factory.Faker('boolean')
    address = factory.SubFactory(AddressFactory)
    zone_id = factory.Faker('random_int', min=1, max=99)
