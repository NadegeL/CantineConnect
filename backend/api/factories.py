import factory
from datetime import date, timedelta
from faker import Faker
from .models import User, Parent, Student, Address, Allergy, Holidays, SchoolZone, Administration


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    address_line_1 = factory.Faker('street_address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory.Faker('country')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    
class AdministrationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Administration

    user = factory.SubFactory(UserFactory)
    is_admin = True
    invoice_edited = False
    address = factory.SubFactory(AddressFactory)

class AllergyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Allergy

    name = factory.Sequence(lambda n: f'Allergie_{n}')
    severity = factory.Iterator(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'])
    description = factory.Faker('text', max_nb_chars=200)


class ParentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Parent

    user = factory.SubFactory(UserFactory)
    address = factory.SubFactory(AddressFactory)
    phone_number = factory.Faker('phone_number')
    is_admin = False
    invoice_available = False


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    birth_date = factory.Faker('date_of_birth')
    grade = factory.Iterator(['CP', 'CE1', 'CE2', 'CM1', 'CM2'])

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
            

class SchoolZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SchoolZone

    name = factory.Iterator(['A', 'B', 'C'])

class HolidaysFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holidays
    
    zone = factory.SubFactory(SchoolZoneFactory)
    start_date = factory.Faker('date_this_year')
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=14))
    description = factory.Faker('sentence')
    school_year = factory.LazyAttribute(lambda _: f"{date.today().year}-{date.today().year + 1}")
