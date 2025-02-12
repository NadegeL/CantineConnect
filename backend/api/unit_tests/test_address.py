from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Address
from api.factories import AddressFactory


class AddressTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.address_data = {
            'address_line_1': '123 Rue de la Paix',
            'address_line_2': 'Appartement 4',
            'city': 'Paris',
            'postal_code': '75000',
            'country': 'France'
        }
        self.url = reverse('address-list')

    def test_create_address(self):
        response = self.client.post(self.url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(Address.objects.get().address_line_1,
                         '123 Rue de la Paix')

    def test_create_address_missing_field(self):
        invalid_data = self.address_data.copy()
        invalid_data.pop('address_line_1')
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_address_list(self):
        self.client.post(self.url, self.address_data, format='json')
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_address_detail(self):
        address = AddressFactory()
        url_detail = reverse('address-detail', kwargs={'pk': address.id})
        response = self.client.get(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['address_line_1'], address.address_line_1)

    def test_update_address(self):
        address = AddressFactory()
        url_detail = reverse('address-detail', kwargs={'pk': address.id})
        updated_data = {'address_line_1': '456 Rue de la Paix'}
        response = self.client.patch(url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Address.objects.get().address_line_1,
                         '456 Rue de la Paix')

    def test_delete_address(self):
        address = AddressFactory()
        url_detail = reverse('address-detail', kwargs={'pk': address.id})
        response = self.client.delete(url_detail, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 0)

    def test_create_duplicate_address(self):
        # Create the first address
        response = self.client.post(self.url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 1)

        # Attempt to create an identical address
        response = self.client.post(self.url, self.address_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 2)
