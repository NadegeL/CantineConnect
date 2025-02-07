from django.test import TestCase
from api.models import Parent, User, Address
from api.factories import ParentFactory, UserFactory, AddressFactory
from django.core.exceptions import ValidationError

class ParentModelTest(TestCase):
    def test_create_parent(self):
        # Créer une instance d'adresse
        address = AddressFactory()

        # Créer une instance d'utilisateur
        user = UserFactory()

        # Créer une instance de parent associée à l'utilisateur et à l'adresse
        parent = ParentFactory(user=user, address=address)

        # Vérifier que l'instance est de type Parent
        self.assertIsInstance(parent, Parent)

        # Vérifier que l'utilisateur associé est créé
        self.assertIsNotNone(parent.user)

        # Vérifier que l'adresse associée est créée
        self.assertIsNotNone(parent.address)

        # Vérifier que certaines informations sont présentes
        self.assertTrue(hasattr(parent, 'phone_number'))
        self.assertEqual(parent.address, address)

    def test_str_method(self):
        # Créer une instance d'adresse
        address = AddressFactory()

        # Créer une instance d'utilisateur
        user = UserFactory()

        # Créer une instance de parent associée à l'utilisateur et à l'adresse
        parent = ParentFactory(user=user, address=address)

        # Tester la méthode __str__() qui retourne le nom du parent
        self.assertEqual(str(parent), f"{parent.user.first_name} {parent.user.last_name}")

    def test_parent_user_link(self):
        # Créer une instance d'adresse
        address = AddressFactory()

        # Créer une instance d'utilisateur
        user = UserFactory()

        # Créer une instance de parent associée à l'utilisateur et à l'adresse
        parent = ParentFactory(user=user, address=address)

        # Vérifier que l'instance d'utilisateur est correctement associée au parent
        self.assertEqual(user, parent.user)

    def test_invalid_email(self):
        # Définir un email invalide
        invalid_email = "invalidemail"

        # Créer une instance d'adresse
        address = AddressFactory()

        # Créer une instance d'utilisateur avec l'email invalide
        user = UserFactory(email=invalid_email)

        # Créer une instance de parent associée à l'utilisateur et à l'adresse
        parent = ParentFactory(user=user, address=address)

        # Vérifier que l'email est valide
        with self.assertRaises(ValidationError):
            parent.full_clean()
