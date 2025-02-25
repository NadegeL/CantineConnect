from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import SchoolClass
from api.factories import SchoolClassFactory


class SchoolClassTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.school_class_data = {
            'name': 'CM2',
            'is_active': True
        }
        self.url = reverse('schoolclass-list')

    def test_create_school_class(self):
        response = self.client.post(
            self.url, self.school_class_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SchoolClass.objects.count(), 1)
        self.assertEqual(SchoolClass.objects.get().name, 'CM2')

    def test_create_school_class_missing_field(self):
        invalid_data = self.school_class_data.copy()
        invalid_data.pop('name')
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_school_class_list(self):
        self.client.post(self.url, self.school_class_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_school_class_detail(self):
        school_class = SchoolClassFactory()
        url_detail = reverse('schoolclass-detail',
                             kwargs={'pk': school_class.id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], school_class.name)

    def test_update_school_class(self):
        school_class = SchoolClassFactory()
        url_detail = reverse('schoolclass-detail',
                             kwargs={'pk': school_class.id})
        updated_data = {'name': 'CM1'}
        response = self.client.patch(url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(SchoolClass.objects.get().name, 'CM1')

    def test_delete_school_class(self):
        school_class = SchoolClassFactory()
        url_detail = reverse('schoolclass-detail',
                             kwargs={'pk': school_class.id})
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SchoolClass.objects.count(), 0)

    def test_create_duplicate_school_class(self):
        # Create the first school class
        response = self.client.post(
            self.url, self.school_class_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SchoolClass.objects.count(), 1)

        # Attempt to create an identical school class
        response = self.client.post(
            self.url, self.school_class_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SchoolClass.objects.count(), 1)
