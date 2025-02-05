import factory
from api.models import User, Parent, Student, Administration
from django.contrib.auth.hashers import make_password

# Factory for User
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    password = factory.Faker('password')
    email = factory.Faker('email')

# Factory for Parent
class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number', locale='en_US')  # Limiter à 20 caractères
    address_line_1 = factory.Faker('address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')

# Factory for Student
class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    birth_date = factory.Faker('date_of_birth')
    grade = factory.Faker('word')
    parent = factory.SubFactory(ParentFactory)

# Factory for Administration
class AdministrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administration

    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.LazyFunction(lambda: make_password('securepassword123'))
    is_admin = True
    address_line_1 = factory.Faker('address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')
    zone_id = factory.Faker('random_int', min=1, max=9999999999)  # Assurez-vous que la valeur est inférieure à 10 caractères
