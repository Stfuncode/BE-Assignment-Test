from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch

# DRF
from rest_framework import status

# models
from .models import Inventory, Supplier

# exceptions
from . import exceptions

# services
from .services import InventoryService


class InventoryServiceTestCase(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier 1"
        )

        self.inventory_1 = Inventory.objects.create(
            name="Item 1",
            description="this is item 1",
            note="test test",
            stock=10,
            availability=True,
            supplier=self.supplier
        )
        self.inventory_2 = Inventory.objects.create(
            name="Item 2",
            description="this is item 2",
            note="this is item 2",
            stock=5,
            availability=False,
            supplier=self.supplier
        )

        self.service = InventoryService()

    @patch('inventory.services.Inventory.objects.filter')
    def test_get_inventories_success(self, mock_filter):
        mock_filter.return_value = [self.inventory_1, self.inventory_2]

        result = self.service.get_inventories(name='Item')

        self.assertEqual(len(result), 2)
        self.assertIn(self.inventory_1, result)
        self.assertIn(self.inventory_2, result)

    @patch('inventory.services.Inventory.objects.filter')
    def test_get_inventories_not_found(self, mock_filter):
        mock_filter.return_value = []

        with self.assertRaises(exceptions.NotFound):
            self.service.get_inventories(name='asdasdsd')

    @patch('inventory.services.Inventory.objects.get')
    def test_get_inventory_success(self, mock_get):
        mock_get.return_value = self.inventory_1

        result = self.service.get_inventory(self.inventory_1.id)

        self.assertEqual(result, self.inventory_1)

    @patch('inventory.services.Inventory.objects.get')
    def test_get_inventory_not_found(self, mock_get):
        mock_get.side_effect = Inventory.DoesNotExist

        with self.assertRaises(exceptions.NotFound):
            self.service.get_inventory(999)

    @patch('inventory.services.Inventory.objects.filter')
    def test_get_inventories_with_filters(self, mock_filter):
        mock_filter.return_value = [self.inventory_1]

        result = self.service.get_inventories(
            name='Item 1', 
            supplier='Supplier 1', 
            stock=10, 
            availability='True'
        )

        self.assertEqual(len(result), 1)
        self.assertIn(self.inventory_1, result)



class InventoryListViewTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier 1"
        )

        self.inventory_1 = Inventory.objects.create(
            name="Item 1",
            description="this is item 1",
            note="test test",
            stock=10,
            availability=True,
            supplier=self.supplier
        )
        self.inventory_2 = Inventory.objects.create(
            name="Item 2",
            description="this is item 2",
            note="this is item 2",
            stock=5,
            availability=False,
            supplier=self.supplier
        )

    def test_inventory_list_view(self):
        url = reverse('inventory_list')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.inventory_1.name)
        self.assertContains(response, self.inventory_2.name)

        self.assertTemplateUsed(response, 'inventory/inventory_list.html')
    


class InventoryDetailViewTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier 1"
        )

        self.inventory = Inventory.objects.create(
            name="Item 1",
            description="this is item 1",
            note="test test",
            stock=10,
            availability=True,
            supplier=self.supplier
        )

    def test_inventory_detail_view(self):
        url = reverse('inventory_detail', kwargs={'id': self.inventory.id})
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['inventory'], self.inventory)

        self.assertTemplateUsed(response, 'inventory/inventory_detail.html')

    def test_inventory_detail_view_not_found(self):
        url = reverse('inventory_detail', kwargs={'id': 9999})
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)



class InventoryApiListViewTest(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Supplier 1"
        )

        self.inventory_1 = Inventory.objects.create(
            name="Item 1",
            description="this is item 1",
            note="test test",
            stock=10,
            availability=True,
            supplier=self.supplier
        )
        self.inventory_2 = Inventory.objects.create(
            name="Item 2",
            description="this is item 2",
            note="this is item 2",
            stock=5,
            availability=False,
            supplier=self.supplier
        )
    
    def test_inventory_api_list_view(self):
        url = '/api/v1/inventory/'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'retrived')
        self.assertEqual(len(data['data']), 2)
        
        self.assertEqual(data['data'][0]['name'], self.inventory_1.name)
        self.assertEqual(data['data'][1]['name'], self.inventory_2.name)

    def test_inventory_api_list_view_with_name_filter(self):
        url = '/api/v1/inventory/?name=Item 1'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()

        data_length = len(data['data'])
        self.assertEqual(data_length, 1)
        self.assertEqual(data['data'][0]['name'], self.inventory_1.name)

    def test_inventory_api_list_view_with_availability_filter(self):
        url = '/api/v1/inventory/?availability=True'

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['name'], self.inventory_1.name)

    def test_inventory_api_list_view_with_non_existing_filter(self):
        url = '/api/v1/inventory/?supplier=aaaaa'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
