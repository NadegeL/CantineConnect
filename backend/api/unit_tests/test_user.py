from django.test import TestCase
from api.models import User, Parent, Address
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_create_user(self):
        # New user creation test
        user = User.objects.create_user(
            email="john_doe@example.com",
            password="password123"
        )
        # Checks that the object created is an instance of User
        self.assertIsInstance(user, User)
        # Checks that the email is correctly defined
        self.assertEqual(user.email, "john_doe@example.com")
        # Checks that the password is set correctly
        self.assertTrue(user.check_password("password123"))

    def test_user_email_unique(self):
        # Create a user with a unique email
        User.objects.create_user(
            password="password123",
            email="uniqueemail@example.com"
        )
        # Attempt to create another user with the same email and assert that it raises an IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                password="password123",
                email="uniqueemail@example.com"
            )

    def test_user_parent_relation(self):
        # Create a user
        user = User.objects.create_user(
            email="email", password="password123")

        # Create an Address first, as it's needed by the Parent model
        address = Address.objects.create(
            address_line_1="123 Main St",
            city="Paris",
            postal_code="75000",
            country="France"
        )

        # Create a parent associated with the user, using the created Address
        parent = Parent.objects.create(
            user=user, phone_number="+33123456789", address=address)

        # Verify that the parent's user field matches the created user
        self.assertEqual(parent.user, user)
        # Verify that the parent's address field is correctly set
        self.assertEqual(parent.address, address)
