from django.test import TestCase
from api.models import User, Parent, Address
from django.db.utils import IntegrityError

class UserModelTest(TestCase):
    def test_create_user(self):
        # Test creating a new user
        user = User.objects.create_user(
            username="john_doe",
            password="password123"
        )
        # Verify that the created object is an instance of User
        self.assertIsInstance(user, User)
        # Verify that the username is correctly set
        self.assertEqual(user.username, "john_doe")
        # Verify that the password is correctly set
        self.assertTrue(user.check_password("password123"))

    def test_user_email_unique(self):
        # Create a user with a unique email
        User.objects.create_user(
            username="user1",
            password="password123",
            email="uniqueemail@example.com"
        )
        # Attempt to create another user with the same email and assert that it raises an IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                username="user2",
                password="password123",
                email="uniqueemail@example.com"
            )

    def test_user_parent_relation(self):
        # Create a user
        user = User.objects.create_user(username="parent_user", password="password123")

        # Create an Address first, as it's needed by the Parent model
        address = Address.objects.create(
            address_line_1="123 Main St",
            city="Paris",
            postal_code="75000",
            country="France"
        )

        # Create a parent associated with the user, using the created Address
        parent = Parent.objects.create(user=user, phone_number="12345", address=address)

        # Verify that the parent's user field matches the created user
        self.assertEqual(parent.user, user)
        # Verify that the parent's address field is correctly set
        self.assertEqual(parent.address, address)
