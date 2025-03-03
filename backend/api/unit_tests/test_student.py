from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Student, Parent, SchoolClass, Allergy, User, Address



class StudentTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Create an Address
        self.address = Address.objects.create(
            address_line_1='123 Rue de la Paix',
            address_line_2='Appartement 4',
            city='Paris',
            postal_code='75000',
            country='France'
        )

        # Create a User
        self.user = User.objects.create_user(
            email='parent@example.com',
            password='securepassword123',
            first_name='John',
            last_name='Doe'
        )

        # Create a Parent
        self.parent = Parent.objects.create(
            user=self.user,
            phone_number='+33123456789',
            country_code='FR',
            invoice_available=True,
            address=self.address,
            is_activated=False
        )

        # Create a second Parent for multi-parent tests
        self.user2 = User.objects.create_user(
            email='parent2@example.com',
            password='securepassword123',
            first_name='Jane',
            last_name='Doe'
        )

        self.parent2 = Parent.objects.create(
            user=self.user2,
            phone_number='+33987654321',
            country_code='FR',
            invoice_available=True,
            address=self.address,
            is_activated=False
        )

        # Create a SchoolClass
        self.school_class = SchoolClass.objects.create(name='CM2')

        # Create an Allergy
        self.allergy = Allergy.objects.create(
            name='Pollen', description='Allergie au pollen', severity='LOW')

        self.student_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'parents': [self.parent.id, self.parent2.id],
            'grade': self.school_class.id,
            'birth_date': '2010-01-01',
            'allergies': [self.allergy.id]
        }

        self.url = reverse('student-list')

    def test_create_student(self):
        response = self.client.post(self.url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Student.objects.get().first_name, 'John')

    def test_create_student_missing_field(self):
        invalid_data = self.student_data.copy()
        invalid_data.pop('first_name')
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_student_list(self):
        self.client.post(self.url, self.student_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_student_detail(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date='2010-01-01',
            grade=self.school_class
        )
        student.parents.set([self.parent, self.parent2])
        student.allergies.set([self.allergy])

        url_detail = reverse('student-detail', kwargs={'pk': student.id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_update_student(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date='2010-01-01',
            grade=self.school_class
        )
        student.parents.set([self.parent, self.parent2])
        student.allergies.set([self.allergy])

        url_detail = reverse('student-detail', kwargs={'pk': student.id})
        updated_data = {'first_name': 'Jane'}
        response = self.client.patch(url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Student.objects.get().first_name, 'Jane')

    def test_delete_student(self):
        student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            birth_date='2010-01-01',
            grade=self.school_class
        )
        student.parents.set([self.parent, self.parent2])
        student.allergies.set([self.allergy])

        url_detail = reverse('student-detail', kwargs={'pk': student.id})
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)

    def test_create_identical_students(self):
        # Create the first student
        response = self.client.post(self.url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Attempt to create an identical student
        response = self.client.post(self.url, self.student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
