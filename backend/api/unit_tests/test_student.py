from django.test import TestCase
from api.models import Student, Parent, User

class StudentModelTest(TestCase):
    def test_create_student(self):
        # Create a user instance
        user = User.objects.create_user(username="student_user", password="password123", first_name="John", last_name="Doe")

        # Create a parent instance associated with the user
        parent = Parent.objects.create(user=user, email="parent@example.com", phone_number="12345", address_line_1="123 Main St", city="Paris", postal_code="75000", country="France")

        # Create a student instance associated with the parent
        student = Student.objects.create(birth_date="2010-01-01", grade="5", parent=parent)

        # Verify that the instance is of type Student
        self.assertIsInstance(student, Student)

        # Verify that the student is associated with the correct parent
        self.assertEqual(student.parent, parent)

        # Verify that the student's grade is correctly set
        self.assertEqual(student.grade, "5")

        # Verify that the __str__() method returns the expected string
        self.assertEqual(str(student), f"{parent.user.first_name} {parent.user.last_name} - 5")

    def test_student_without_parent(self):
        # Create a student instance without a parent
        student = Student.objects.create(birth_date="2010-01-01", grade="5")

        # Verify that the student's parent is None
        self.assertIsNone(student.parent)

        # Verify that the student's grade is correctly set
        self.assertEqual(student.grade, "5")

        # Verify that the __str__() method returns the expected string when the parent is None
        self.assertEqual(str(student), " - 5")
