from django.test import TestCase
from api.models import Parent, User, Address
from api.factories import ParentFactory, UserFactory, AddressFactory
from django.core.exceptions import ValidationError

class ParentModelTest(TestCase):
    def test_create_parent(self):
        # Create an address instance
        address = AddressFactory()

        # Create a user instance
        user = UserFactory()

        # Create a parent instance associated with the user and address
        parent = ParentFactory(user=user, address=address)

        # Check that the instance is of type Parent
        self.assertIsInstance(parent, Parent)

        # Check that the associated user has been created
        self.assertIsNotNone(parent.user)

        # Check that the associated address has been created
        self.assertIsNotNone(parent.address)

        # Check that certain information is present
        self.assertTrue(hasattr(parent, 'phone_number'))
        self.assertEqual(parent.address, address)

    def test_str_method(self):
        # Create an address instance
        address = AddressFactory()

        # Create a user instance
        user = UserFactory()

        # Create a parent instance associated with the user and address
        parent = ParentFactory(user=user, address=address)

        # Test the __str__() method, which returns the parent's name
        self.assertEqual(str(parent), f"{parent.user.first_name} {parent.user.last_name}")

    def test_parent_user_link(self):
        # Create an address instance
        address = AddressFactory()

        # Create a user instance
        user = UserFactory()

        # Create a parent instance associated with the user and address
        parent = ParentFactory(user=user, address=address)

        # Check that the user instance is correctly associated with the parent
        self.assertEqual(user, parent.user)

    def test_invalid_email(self):
        # Define an invalid email
        invalid_email = "invalidemail"

        # Create an address instance
        address = AddressFactory()

        # Create a user instance with an invalid email address
        user = UserFactory(email=invalid_email)

        # Create a parent instance associated with the user and address
        parent = ParentFactory(user=user, address=address)

        # Check that the email is valid
        with self.assertRaises(ValidationError):
            parent.full_clean()
