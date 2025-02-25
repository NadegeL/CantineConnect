from django.test import TestCase
from api.models import Administration, SchoolZone
from api.factories import UserFactory, AdministrationFactory, SchoolZoneFactory, AddressFactory
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class AdministrationModelTest(TestCase):
    def test_create_administration(self):
        zone = SchoolZoneFactory(name='A')
        admin = AdministrationFactory(user__is_staff=True, zone=zone)
        self.assertIsInstance(admin, Administration)
        self.assertTrue(hasattr(admin, 'user'))
        self.assertTrue(hasattr(admin, 'address'))
        self.assertTrue(hasattr(admin, 'zone'))
        self.assertTrue(admin.is_admin)

    def test_str_method(self):
        admin = AdministrationFactory(user__is_staff=True)
        self.assertEqual(
            str(admin), f"{admin.user.first_name} {admin.user.last_name}")

    def test_admin_zone(self):
        admin = AdministrationFactory(user__is_staff=True)
        self.assertTrue(hasattr(admin, 'zone'))
        self.assertIsNotNone(admin.zone)
        self.assertIsInstance(admin.zone, SchoolZone)

    def test_duplicate_administration(self):
        user = UserFactory(is_staff=True)
        AdministrationFactory(user=user)
        with self.assertRaises(IntegrityError):
            AdministrationFactory(user=user)

    def test_update_administration(self):
        admin = AdministrationFactory(user__is_staff=True)
        new_zone = SchoolZoneFactory(name='B')
        admin.zone = new_zone
        admin.save()
        admin.refresh_from_db()
        self.assertEqual(admin.zone, new_zone)


    def test_delete_administration(self):
        admin = AdministrationFactory(user__is_staff=True)
        admin_id = admin.id
        admin.delete()
        self.assertFalse(Administration.objects.filter(id=admin_id).exists())


    def test_invalid_zone(self):
        with self.assertRaises(ValidationError):
            zone = SchoolZoneFactory.build(name='X')
            zone.full_clean()


    def test_invalid_zone_id(self):
        user = UserFactory(is_staff=True)
        address = AddressFactory()
        with self.assertRaises(ValidationError):
            admin = Administration(user=user, address=address,
                                zone=SchoolZoneFactory(name='X'))
            admin.full_clean()



    def test_invalid_email(self):
        # Defines an invalid email
        invalid_email = "invalidemail"

        # Creates a user instance with invalid email
        admin = AdministrationFactory(
            user__email=invalid_email, user__is_staff=True)

        # Checks that email validation raises a ValidationError
        with self.assertRaises(ValidationError):
            admin.user.full_clean()
