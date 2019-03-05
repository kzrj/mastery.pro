from mixer.backend.django import mixer

from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse

from product.models import Product, Supplier, Articul, Customer


class ProductViewsTest(TestCase):
    # fixtures = ['test_data', ]

    def setUp(self):
        user = User.objects.create_user(username='test_supplier1')
        self.supplier1 = Supplier.objects.create(user=user)

        user = User.objects.create_user(username='test_customer1', password='qwerty123')
        self.customer1 = Customer.objects.create(user=user)

        self.superuser = User.objects.create_superuser(username='test_admin',
         password='qwerty123', email='')

        self.client = Client()

    def test_supplier_regular_page_permissions(self):
        # GET by Anonimous
        response = self.client.get(reverse('supplier-regular-page'))
        self.assertEqual(response.status_code, 302)

    def test_supplier_regular_page(self):
        # login = self.client.login(username='test_supplier1', password='qwerty123')
        login = self.client.login(username='test_supplier1', password=self.customer1.user.password)
        # self.client.force_login(self.customer1.user, backend=None)
        print(self.client)
        print(login)
        print(User.objects.filter(username='test_supplier1'))
        response = self.client.get(reverse('supplier-regular-page'), {'user_id': self.customer1.user.id})
        print(response)
        self.assertEqual(response.status_code, 200)


