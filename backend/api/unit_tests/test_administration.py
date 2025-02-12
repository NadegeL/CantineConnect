from django.test import TestCase
from api.models import Administration
from api.factories import UserFactory, AdministrationFactory
from django.core.exceptions import ValidationError
from django.db import IntegrityError, DataError


class AdministrationModelTest(TestCase):
    def test_create_administration(self):
        # Creates an administration instance using the factory with is_staff=True
        admin = AdministrationFactory(user__is_staff=True)

        # Checks that the instance is of type Administration
        self.assertIsInstance(admin, Administration)

        # Checks that certain attributes are present
        self.assertTrue(hasattr(admin, 'user'))
        self.assertTrue(hasattr(admin, 'address'))

        # Checks that the 'is_admin' field is set to True
        self.assertTrue(admin.is_admin)

    def test_str_method(self):
        # Creates an administration instance using the factory with is_staff=True
        admin = AdministrationFactory(user__is_staff=True)

        # Tests the __str__() method, which returns the admin's full name
        self.assertEqual(
            str(admin), f"{admin.user.first_name} {admin.user.last_name}")

    def test_admin_zone_id(self):
        # Creates an administration instance using the factory with is_staff=True
        admin = AdministrationFactory(user__is_staff=True)

        # Checks that the zone_id attribute is set and not None
        self.assertTrue(hasattr(admin, 'zone_id'))
        self.assertIsNotNone(admin.zone_id)

    def test_invalid_email(self):
        # Defines an invalid email
        invalid_email = "invalidemail"

        # Creates a user instance with invalid email
        admin = AdministrationFactory(
            user__email=invalid_email, user__is_staff=True)

        # Checks that email validation raises a ValidationError
        with self.assertRaises(ValidationError):
            admin.user.full_clean()

    def test_duplicate_administration(self):
        # Creates a user with is_staff=True
        user = UserFactory(is_staff=True)

        # Creates an administration instance
        admin1 = AdministrationFactory(user=user)

        # Attempts to create another administration with the same user
        with self.assertRaises(IntegrityError):
            admin2 = AdministrationFactory(user=user)

    def test_invalid_zone_id(self):
        # Creates a user with is_staff=True
        user = UserFactory(is_staff=True)

        # Attempts to create an administration with an invalid zone_id
        with self.assertRaises(DataError):
            admin = AdministrationFactory(user=user, zone_id='INVALID_ZONE')

    def test_update_administration(self):
        # Creates an administration instance
        admin = AdministrationFactory(user__is_staff=True)

        # Updates the administration instance
        new_zone_id = 'A'
        admin.zone_id = new_zone_id
        admin.save()

        # Refreshes the instance from the database
        admin.refresh_from_db()

        # Checks that the zone_id is updated
        self.assertEqual(admin.zone_id, new_zone_id)

    def test_delete_administration(self):
        # Creates an administration instance
        admin = AdministrationFactory(user__is_staff=True)

        # Deletes the administration instance
        admin.delete()

        # Checks that the administration instance is deleted
        self.assertFalse(Administration.objects.filter(pk=admin.pk).exists())
