from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Category, Tag


class ProductSearchAndFilterAPITests(APITestCase):
    
    def setUp(self):
        # Create categories
        self.electronics = Category.objects.create(name="Electronics")
        self.clothing = Category.objects.create(name="Clothing")
        self.books = Category.objects.create(name="Books")
        
        # Create tags
        self.new_tag = Tag.objects.create(name="new")
        self.sale_tag = Tag.objects.create(name="sale")
        self.premium_tag = Tag.objects.create(name="premium")
        self.discounted_tag = Tag.objects.create(name="discounted")
        
        # Create products
        self.product1 = Product.objects.create(
            name="iPhone 13",
            description="Latest smartphone with advanced features and great camera",
            price=999.99
        )
        self.product1.categories.add(self.electronics)
        self.product1.tags.add(self.new_tag, self.premium_tag)
        
        self.product2 = Product.objects.create(
            name="Samsung Galaxy",
            description="Android smartphone with excellent display",
            price=799.99
        )
        self.product2.categories.add(self.electronics)
        self.product2.tags.add(self.sale_tag)
        
        self.product3 = Product.objects.create(
            name="Cotton T-Shirt",
            description="Comfortable cotton t-shirt for everyday wear",
            price=29.99
        )
        self.product3.categories.add(self.clothing)
        self.product3.tags.add(self.new_tag, self.sale_tag)
        
        self.product4 = Product.objects.create(
            name="Python Programming Book",
            description="Learn Python programming with this comprehensive guide",
            price=49.99
        )
        self.product4.categories.add(self.books)
        self.product4.tags.add(self.new_tag)
        
        self.product5 = Product.objects.create(
            name="Wireless Headphones",
            description="Noise cancelling wireless headphones",
            price=199.99
        )
        self.product5.categories.add(self.electronics)
        self.product5.tags.add(self.premium_tag)
        
        self.url = reverse('products_list')
    

    def test_search_by_description_basic(self):
        response = self.client.get(self.url, {'search': 'smartphone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # iPhone and Samsung
        
        product_names = [product['name'] for product in response.data]
        self.assertIn('iPhone 13', product_names)
        self.assertIn('Samsung Galaxy', product_names)
    

    def test_search_by_description_partial_match(self):
        response = self.client.get(self.url, {'search': 'phone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # iPhone, Samsung, Wireless Headphones
    

    def test_search_by_description_case_insensitive(self):
        response = self.client.get(self.url, {'search': 'SMARTPHONE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    

    def test_search_by_description_no_results(self):
        response = self.client.get(self.url, {'search': 'nonexistentproduct'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    

    def test_search_by_description_empty_string(self):
        response = self.client.get(self.url, {'search': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return all products
        self.assertEqual(len(response.data), 5)
    

    def test_filter_by_single_category(self):
        response = self.client.get(self.url, {'category': self.electronics.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # iPhone, Samsung, Headphones
        
        product_names = [product['name'] for product in response.data]
        self.assertIn('iPhone 13', product_names)
        self.assertIn('Samsung Galaxy', product_names)
        self.assertIn('Wireless Headphones', product_names)
    

    def test_filter_by_multiple_categories(self):
        response = self.client.get(
            self.url, 
            {'category': f'{self.electronics.id},{self.clothing.id}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All except books
    

    def test_filter_by_nonexistent_category(self):
        response = self.client.get(self.url, {'category': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    

    def test_filter_by_invalid_category_id(self):
        response = self.client.get(self.url, {'category': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_filter_by_single_tag(self):
        response = self.client.get(self.url, {'tag': self.new_tag.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # iPhone, T-Shirt, Book
        
        product_names = [product['name'] for product in response.data]
        self.assertIn('iPhone 13', product_names)
        self.assertIn('Cotton T-Shirt', product_names)
        self.assertIn('Python Programming Book', product_names)
    

    def test_filter_by_multiple_tags(self):
        response = self.client.get(
            self.url, 
            {'tag': f'{self.new_tag.id},{self.sale_tag.id}'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All except headphones
    

    def test_filter_by_nonexistent_tag(self):
        response = self.client.get(self.url, {'tag': 999})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


    def test_filter_by_invalid_tag_id(self):
        response = self.client.get(self.url, {'tag': 'invalid'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_combined_search_and_filters(self):
        response = self.client.get(
            self.url, 
            {
                'search': 'phone',
                'category': self.electronics.id,
                'tag': self.new_tag.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only iPhone 13
        print(response.data)
        self.assertEqual(response.data[0]['name'], 'iPhone 13')
    

    def test_no_parameters_returns_all(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
    

    def test_whitespace_handling(self):
        response = self.client.get(self.url, {'search': '  smartphone  '})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    

    def test_empty_database(self):
        Product.objects.all().delete()
        response = self.client.get(self.url, {'search': 'smartphone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    

    def test_response_structure(self):
        response = self.client.get(self.url, {'search': 'iPhone'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        if len(response.data) > 0:
            product = response.data[0]
            expected_fields = ['id', 'name', 'description', 'price', 'categories', 'tags']
            for field in expected_fields:
                self.assertIn(field, product)
