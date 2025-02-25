from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Parent, User, Address
from api.factories import ParentFactory, UserFactory, AddressFactory


class ParentTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.address = AddressFactory()
        self.user = UserFactory()
        self.parent_data = {
            'user': self.user.id,
            'phone_number': '+33123456789',
            'country_code': 'FR',
            'is_admin': False,
            'invoice_available': False,
            'address': self.address.id,
            'is_activated': False,
            'relation': 'Mère'
        }
        self.url = reverse('parent-list')

    def test_create_parent(self):
        response = self.client.post(self.url, self.parent_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parent.objects.count(), 1)
        self.assertEqual(Parent.objects.get().relation, 'Mère')

    def test_create_parent_missing_field(self):
        invalid_data = self.parent_data.copy()
        invalid_data.pop('phone_number')
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_parent_list(self):
        self.client.post(self.url, self.parent_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_parent_detail(self):
        parent = ParentFactory()
        url_detail = reverse('parent-detail', kwargs={'pk': parent.id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['relation'], parent.relation)

    def test_update_parent(self):
        parent = ParentFactory()
        url_detail = reverse('parent-detail', kwargs={'pk': parent.id})
        updated_data = {'relation': 'Père'}
        response = self.client.patch(url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Parent.objects.get().relation, 'Père')

    def test_delete_parent(self):
        parent = ParentFactory()
        url_detail = reverse('parent-detail', kwargs={'pk': parent.id})
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Parent.objects.count(), 0)

    def test_create_duplicate_parent(self):
        # Create the first parent
        response = self.client.post(self.url, self.parent_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parent.objects.count(), 1)

        # Create a new user for the second parent
        new_user = UserFactory()
        duplicate_parent_data = self.parent_data.copy()
        duplicate_parent_data['user'] = new_user.id

        # Attempt to create an identical parent with a different user
        response = self.client.post(
            self.url, duplicate_parent_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parent.objects.count(), 2)
