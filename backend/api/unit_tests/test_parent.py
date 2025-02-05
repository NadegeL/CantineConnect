from django.test import TestCase
from api.models import Parent, User
from api.factories import ParentFactory, UserFactory
from django.core.exceptions import ValidationError

class ParentModelTest(TestCase):
    def test_create_parent(self):
        # Create a parent instance using the factory
        parent = ParentFactory()

        # Verify that the instance is of type Parent
        self.assertIsInstance(parent, Parent)

        # Verify that the associated user is created
        self.assertIsNotNone(parent.user)

        # Verify that certain information is present
        self.assertTrue(hasattr(parent, 'email'))
        self.assertTrue(hasattr(parent, 'phone_number'))
        self.assertTrue(hasattr(parent, 'address_line_1'))
        self.assertTrue(hasattr(parent, 'city'))

    def test_str_method(self):
        # Create a parent instance using the factory
        parent = ParentFactory()
        # Test the __str__() method which returns the parent's name
        self.assertEqual(str(parent), f"{parent.user.first_name} {parent.user.last_name}")

    def test_parent_user_link(self):
        # Create a parent instance using the factory
        parent = ParentFactory()
        user = parent.user
        # Verify that the User instance is correctly associated with the parent
        self.assertEqual(user, parent.user)

    def test_invalid_email(self):
        # Define an invalid email
        invalid_email = "invalidemail"
        # Create a parent instance with the invalid email
        parent = ParentFactory(email=invalid_email)
        # Verify that the email is valid
        with self.assertRaises(ValidationError):
            parent.full_clean()
