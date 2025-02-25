from django.test import TestCase
from api.factories import AllergyFactory, StudentFactory


class AllergyTests(TestCase):
    def setUp(self):
        self.allergy = AllergyFactory(
            name="Arachides",
            severity="HIGH",
            description="Allergie aux arachides"
        )

    def test_allergy_creation(self):
        """Test la création d'une allergie"""
        self.assertEqual(self.allergy.name, "Arachides")
        self.assertEqual(self.allergy.severity, "HIGH")

    def test_allergy_str_method(self):
        """Test la représentation string de l'allergie"""
        self.assertEqual(str(self.allergy), "Arachides")

    def test_students_with_allergy(self):
        """Test la relation avec les étudiants"""
        student1 = StudentFactory()
        student2 = StudentFactory()
        student1.allergies.add(self.allergy)
        student2.allergies.add(self.allergy)

        students_with_allergy = self.allergy.student_set.all()
        self.assertEqual(students_with_allergy.count(), 2)

    def test_severity_choices(self):
        """Test les choix de sévérité"""
        valid_severities = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        allergy = AllergyFactory(severity='LOW')
        self.assertIn(allergy.severity, valid_severities)
