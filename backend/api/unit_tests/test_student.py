from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from faker import Faker
from django.test import TestCase


class StudentModelTest(TestCase):
    def setUp(self):
        # Initialize the Faker instance for generating fake data
        self.fake = Faker()

    def test_create_student(self):
        # Generate a unique email address using Faker
        email = self.fake.unique.email()
        # Create a new user with the generated email and specified credentials
        student_user = User.objects.create_user(
            username="student_user",
            email=email,
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        # Assert that the user was created successfully and the email matches
        self.assertIsNotNone(student_user.id)
        self.assertEqual(student_user.email, email)

    def test_create_student_without_email(self):
        # Create a new user without specifying an email
        student_user = User.objects.create_user(
            username="student_no_email",
            password="password123",
            first_name="Jane",
            last_name="Doe"
        )
        # Assert that the user was created successfully and the email field is empty
        self.assertIsNotNone(student_user.id)
        self.assertEqual(student_user.email, '')

    def test_username_uniqueness(self):
        # Create a user with a unique username
        User.objects.create_user(
            username="unique_user",
            password="password123",
            first_name="Alice",
            last_name="Smith"
        )
        # Attempt to create another user with the same username and expect an exception
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="unique_user",
                password="password456",
                first_name="Bob",
                last_name="Brown"
            )

    def test_student_str_method(self):
        # Create a user and test the __str__ method
        student_user = User.objects.create_user(
            username="student_str",
            password="password123",
            first_name="Charlie",
            last_name="Davis"
        )
        # Assert that the string representation of the user matches the username
        self.assertEqual(str(student_user), "student_str")

    def test_create_student_without_username(self):
        # Attempt to create a user without a username and expect a ValueError
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="",
                password="password123",
                first_name="Eve",
                last_name="Foster"
            )

    def test_student_authentication(self):
        # Create a user for authentication testing
        User.objects.create_user(
            username="auth_user",
            password="password123",
            first_name="Grace",
            last_name="Hopper"
        )
        # Authenticate the user with the correct credentials
        user = authenticate(username="auth_user", password="password123")
        # Assert that the authentication was successful and the user is authenticated
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)
