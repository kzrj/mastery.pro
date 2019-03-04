from mixer.backend.django import mixer

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.db import connection
from django.conf import settings

from product.models import Product, Supplier


def create_supplier():
    user = mixer.blend('auth.user')
    return Supplier.objects.create(user=user)


class ProductModelUniqueTest(TransactionTestCase):
    def test_articul_unique_charField(self):
        supplier1 = create_supplier()       
        supplier2 = create_supplier()
        
        product1 = Product.objects.create(
            title='First product',
            price=1,
            articul='123',
            supplier=supplier1, is_available=True)

        product2 = Product.objects.create(title='Second product', price=1, articul='123',
                supplier=supplier2, is_available=True)

        with self.assertRaises(IntegrityError):
            product3 = Product.objects.create(title='Third product', price=1, articul='123',
                supplier=supplier1, is_available=True)
        
        with self.assertRaises(IntegrityError):
            product4 = Product.objects.create(title='Forth product', price=1, articul='123',
                    supplier=supplier2, is_available=True)


class ProductManagerTest(TestCase):
    fixtures = ['suppliers_and_products', ]

    def test_compare(self):
        settings.DEBUG = True
        
        supplier1 = Supplier.objects.all().first()
        print(Product.objects.available_and_not_own(supplier1).count())
        print(len(connection.queries))

        print('Method 1')
        for supplier1_product in supplier1.products.all():
            print('Count:', supplier1_product.products_with_same_articul_and_better_price().count())
        print(len(connection.queries))

        print('Method 2')
        for product in Product.objects.available_and_not_own(supplier1):
            print('Count:', supplier1.products.filter(articul=product.articul).filter(price__gt=product.price).count())
        print(len(connection.queries))

        print('Method 3')
        print(len(connection.queries))
        supplier1_products = list(supplier1.products.all())
        for product in Product.objects.available_and_not_own(supplier1): 
            for supplier1_product in supplier1_products:
                print(supplier1_product.price, product.price)
        print(len(connection.queries))

        print('Method 4')
        print(len(connection.queries))
        before = len(connection.queries)
        products = list(Product.objects.available_and_not_own(supplier1))
        for supplier1_product in supplier1.products.all():
            for product in products:
                print(supplier1_product.price, supplier1_product.articul, product.price, product.articul)
        print(before)
        print(len(connection.queries))



        settings.DEBUG = False

        # for p in Product.objects.available_and_not_own(supplier1).distinct('articul'):
        #     # if p.articul == 'eight':
        #         print(p.title, p.articul, p.price)

        # for p in Product.objects.all():
        #     if p.articul == 'eight':
        #         print(p.title, p.articul, p.price, p.is_available)


