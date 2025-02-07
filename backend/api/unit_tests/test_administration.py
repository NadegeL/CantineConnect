from django.test import TestCase
from api.models import Parent, User, Administration
from api.factories import ParentFactory, UserFactory, AdministrationFactory, AddressFactory
from django.core.exceptions import ValidationError


class AdministrationModelTest(TestCase):
    def test_create_administration(self):
        # Creates an administration instance using the factory
        admin = AdministrationFactory()

        # Checks that the instance is of type Administration
        self.assertIsInstance(admin, Administration)

        # Checks that certain attributes are present
        self.assertTrue(hasattr(admin, 'user'))
        self.assertTrue(hasattr(admin, 'address'))

        # Checks that the 'is_admin' field is set to True
        self.assertTrue(admin.is_admin)

    def test_str_method(self):
        # Creates an administration instance using the factory
        admin = AdministrationFactory()

        # Tests the __str__() method, which returns the admin's full name
        self.assertEqual(
            str(admin), f"{admin.user.first_name} {admin.user.last_name}")

    def test_admin_zone_id(self):
        # Creates an administration instance using the factory
        admin = AdministrationFactory()

        # Checks that the zone_id attribute is set and not None
        self.assertTrue(hasattr(admin, 'zone_id'))
        self.assertIsNotNone(admin.zone_id)

    def test_invalid_email(self):
        # Defines an invalid email
        invalid_email = "invalidemail"

        # Creates a user instance with invalid email
        admin = AdministrationFactory(user__email=invalid_email)

        # Checks that email validation raises a ValidationError
        with self.assertRaises(ValidationError):
            admin.user.full_clean()


class ParentModelTest(TestCase):
    def test_create_minimal_parent(self):
        # Creates an address instance using the factory
        address = AddressFactory()

        # Creates a parent instance with minimal information
        user = UserFactory(email="parent@example.com", password="temporary")
        parent = Parent.objects.create(
            user=user, phone_number="+123456789", address=address)

        # Checks that the instance is of type Parent
        self.assertIsInstance(parent, Parent)

        # Checks that the 'is_activated' field is set to False
        self.assertFalse(parent.is_activated)

        # Checks that the activation token is generated
        self.assertIsNotNone(parent.activation_token)

    def test_email_validation(self):
        # Defines an invalid email
        invalid_email = "invalidemail"

        # Creates a user instance with invalid email
        user = UserFactory(email=invalid_email, password="temporary")

        # Checks that email validation raises a ValidationError
        with self.assertRaises(ValidationError):
            user.full_clean()

    def test_activation_token_generation(self):
        # Creates an address instance using the factory
        address = AddressFactory()

        # Creates a parent instance
        user = UserFactory(email="parent@example.com", password="temporary")
        parent = Parent.objects.create(
            user=user, phone_number="+123456789", address=address)

        # Checks that the activation token is generated
        self.assertIsNotNone(parent.activation_token)
        self.assertEqual(len(parent.activation_token), 40)

    def test_parent_activation(self):
        # Creates an address instance using the factory
        address = AddressFactory()

        # Creates a parent instance
        user = UserFactory(email="parent@example.com", password="temporary")
        parent = Parent.objects.create(
            user=user, phone_number="+123456789", address=address)

        # Simulates activation
        parent.is_activated = True
        parent.save()

        # Checks that the parent is activated
        self.assertTrue(parent.is_activated)
