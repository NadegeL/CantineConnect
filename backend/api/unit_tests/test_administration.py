from django.test import TestCase
from api.models import Administration
from api.factories import AdministrationFactory
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
        self.assertEqual(str(admin), f"{admin.user.first_name} {admin.user.last_name}")

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

        # Checks that email validation lifts a ValidationError
        with self.assertRaises(ValidationError):
            admin.user.full_clean()

