# -*- coding: utf-8 -*-
import random

from mixer.backend.django import mixer

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from product.models import Product, Supplier, Articul, Customer
# from products.utils import create_products


def create_products(supplier):
    products = list()

    for articul in Articul.objects.all():
        title = 'Product {} {}'.format(articul, supplier.user.username)
        price = random.randint(10, 100)
        is_av = random.choice([True, False])
        products.append(Product(title=title, price=price, articul=articul,
         is_available=is_av, supplier=supplier))

    Product.objects.bulk_create(products)


class ProductViewsTest(TestCase):
    fixtures = ['test_data', ]

    def setUp(self):
        user = User.objects.get(username='test_supplier1')
        self.supplier1 = Supplier.objects.get(user=user)

        user = User.objects.get(username='test_customer1')
        self.customer1 = Customer.objects.get(user=user)

        self.superuser = User.objects.get(username='test_admin')

        self.client = Client()

    def test_suppliers_pages_permissions_anon(self):
        # GET by Anonimous
        response = self.client.get(reverse('supplier-regular-page'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('supplier-comparative-page'))
        self.assertEqual(response.status_code, 403)

    def test_suppliers_pages_permissions_customer(self):
        # GET by customer
        self.client.login(username='test_customer1', password='qwerty123')        
        response = self.client.get(reverse('supplier-regular-page'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('supplier-comparative-page'))
        self.assertEqual(response.status_code, 403)

        self.client.logout()

    def test_suppliers_pages_permissions_admin(self):
        # GET by super
        self.client.login(username='test_admin', password='qwerty123')        
        response = self.client.get(reverse('supplier-regular-page'))
        self.assertEqual(response.status_code, 403)

        response = self.client.get(reverse('supplier-comparative-page'))
        self.assertEqual(response.status_code, 403)

        self.client.logout()

    def test_suppliers_pages_permissions_supplier(self):
        # GET by supplier
        self.client.login(username='test_supplier1', password='qwerty123')        
        response = self.client.get(reverse('supplier-regular-page'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('supplier-comparative-page'))
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_supplier_regular_page(self):
        # Should return own products.
        self.client.login(username='test_supplier1', password='qwerty123')       
        response = self.client.get(reverse('supplier-regular-page'))
        context_products_pk = [ p.pk for p in response.context['products']]
        regular_products_pk = [ p.pk for p in Product.objects.filter(supplier=self.supplier1)]
        self.assertListEqual(context_products_pk, regular_products_pk)
        self.client.logout()

    def test_supplier_comparative_page_check_products(self):
        # Should return own products.
        self.client.login(username='test_supplier1', password='qwerty123')       
        response = self.client.get(reverse('supplier-comparative-page'))
        context_products_pk = [ p['product'].pk for p in response.context['products_with_comparative_list']]
        regular_products_pk = [ p.pk for p in Product.objects.filter(supplier=self.supplier1)]
        self.assertListEqual(context_products_pk, regular_products_pk)
        self.client.logout()

    def test_supplier_comparative_page_comparative_list(self):
        # Should return comparative products list for each own product.
        self.client.login(username='test_supplier1', password='qwerty123')       
        response = self.client.get(reverse('supplier-comparative-page'))

        for product in response.context['products_with_comparative_list']:
            products_with_less_price = products_with_less_price = Product.objects \
                                        .filter(articul=product['product'].articul) \
                                        .filter(is_available=True) \
                                        .filter(price__lt=product['product'].price)
            self.assertListEqual(product['products_with_less_price'],
                 list(products_with_less_price))
        self.client.logout()
        
    def test_customer_page_permissions_anon(self):
        # GET by Anonimous
        response = self.client.get(reverse('customer-page'))
        self.assertEqual(response.status_code, 403)

    def test_customer_page_permissions_admin(self):
        # GET by super
        self.client.login(username='test_admin', password='qwerty123')        
        response = self.client.get(reverse('customer-page'))
        self.assertEqual(response.status_code, 403)

        self.client.logout()

    def test_customer_page_permissions_supplier(self):
        # GET by supplier
        self.client.login(username='test_supplier1', password='qwerty123')        
        response = self.client.get(reverse('customer-page'))
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_customer_page_permissions_customer(self):
        # GET by customer
        self.client.login(username='test_customer1', password='qwerty123')        
        response = self.client.get(reverse('customer-page'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_customer_page_permissions_customer(self):
        # Should return all products
        self.client.login(username='test_customer1', password='qwerty123')        
        response = self.client.get(reverse('customer-page'))

        context_products_pk = [ p.pk for p in response.context['products']]
        regular_products_pk = [ p.pk for p in Product.objects.all()]
        self.assertListEqual(context_products_pk, regular_products_pk)
    
        self.client.logout()
