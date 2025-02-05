from django.test import TestCase
from api.models import Administration
from api.factories import AdministrationFactory
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

class AdministrationModelTest(TestCase):
    def test_create_administration(self):
        # Create an administration instance using the factory
        admin = AdministrationFactory()

        # Verify that the instance is of type Administration
        self.assertIsInstance(admin, Administration)

        # Verify that certain attributes are present
        self.assertTrue(hasattr(admin, 'email'))
        self.assertTrue(hasattr(admin, 'firstname'))
        self.assertTrue(hasattr(admin, 'zone_id'))

        # Verify that the admin flag is set to True
        self.assertTrue(admin.is_admin)

    def test_str_method(self):
        # Create an administration instance using the factory
        admin = AdministrationFactory()

        # Test the __str__() method which returns the admin's full name
        self.assertEqual(str(admin), f"{admin.firstname} {admin.lastname}")

    def test_admin_zone_id(self):
        # Create an administration instance using the factory
        admin = AdministrationFactory()

        # Verify that the zone_id attribute is set and not None
        self.assertTrue(admin.zone_id)
        self.assertIsNotNone(admin.zone_id)

    def test_password_encryption(self):
        # Create an administration instance with a specified password
        admin = AdministrationFactory(password="securepassword123")

        # Verify that the password is correctly encrypted
        self.assertTrue(check_password("securepassword123", admin.password))

    def test_invalid_email(self):
        # Define an invalid email
        invalid_email = "invalidemail"

        # Create an administration instance with the invalid email
        admin = AdministrationFactory(email=invalid_email)

        # Verify that the email validation raises a ValidationError
        with self.assertRaises(ValidationError):
            admin.full_clean()
