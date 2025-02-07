from django.test import TestCase
from api.models import Administration
from api.factories import AdministrationFactory
from django.core.exceptions import ValidationError

class AdministrationModelTest(TestCase):
    def test_create_administration(self):
        # Crée une instance d'administration en utilisant la factory
        admin = AdministrationFactory()

        # Vérifie que l'instance est de type Administration
        self.assertIsInstance(admin, Administration)

        # Vérifie que certains attributs sont présents
        self.assertTrue(hasattr(admin, 'user'))
        self.assertTrue(hasattr(admin, 'address'))

        # Vérifie que le champ 'is_admin' est défini sur True
        self.assertTrue(admin.is_admin)

    def test_str_method(self):
        # Crée une instance d'administration en utilisant la factory
        admin = AdministrationFactory()

        # Teste la méthode __str__() qui retourne le nom complet de l'admin
        self.assertEqual(str(admin), f"{admin.user.first_name} {admin.user.last_name}")

    def test_admin_zone_id(self):
        # Crée une instance d'administration en utilisant la factory
        admin = AdministrationFactory()

        # Vérifie que l'attribut zone_id est défini et n'est pas None
        self.assertTrue(hasattr(admin, 'zone_id'))
        self.assertIsNotNone(admin.zone_id)

    def test_invalid_email(self):
        # Définit un email invalide
        invalid_email = "invalidemail"

        # Crée une instance d'utilisateur avec l'email invalide
        admin = AdministrationFactory(user__email=invalid_email)

        # Vérifie que la validation de l'email lève une ValidationError
        with self.assertRaises(ValidationError):
            admin.user.full_clean()

