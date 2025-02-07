from django.test import TestCase
from api.models import Student, Parent, User, Address

class StudentModelTest(TestCase):
    def test_create_student(self):
        # Créer une instance de User pour le parent
        parent_user = User.objects.create_user(username="parent_user", password="password123", first_name="Jane", last_name="Doe")

        # Créer une instance de Address pour le parent
        address = Address.objects.create(address_line_1="123 Main St", city="Paris", postal_code="75000", country="France")

        # Créer une instance de Parent associée à l'utilisateur et à l'adresse
        parent = Parent.objects.create(user=parent_user, phone_number="12345", address=address)

        # Créer une instance de User pour l'étudiant
        student_user = User.objects.create_user(username="student_user", password="password123", first_name="John", last_name="Doe")

        # Créer une instance de Student sans associer de parents initialement
        student = Student.objects.create(user=student_user, birth_date="2010-01-01", grade="5")

        # Associer le parent à l'étudiant
        student.parents.add(parent)

        # Vérifier que l'instance est de type Student
        self.assertIsInstance(student, Student)

        # Vérifier que l'étudiant est associé au bon parent
        self.assertIn(parent, student.parents.all())

        # Vérifier que le grade de l'étudiant est correctement défini
        self.assertEqual(student.grade, "5")

        # Vérifier que la méthode __str__() renvoie la chaîne attendue
        parent_names = ", ".join([f"{p.user.first_name} {p.user.last_name}" for p in student.parents.all()])
        self.assertEqual(str(student), f"{student.user.first_name} {student.user.last_name} - 5 (Parents: {parent_names})")
