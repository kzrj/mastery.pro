from mixer.backend.django import mixer

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.db import connection
from django.conf import settings

from product.models import Product, Supplier, Articul


def create_supplier():
    user = mixer.blend('auth.user')
    return Supplier.objects.create(user=user)


class ProductModelUniqueTest(TransactionTestCase):
    fixtures = ['articuls', ]

    def test_articul_unique_charField(self):
        supplier1 = create_supplier()       
        supplier2 = create_supplier()
        articul = Articul.objects.all().first()
        
        product1 = Product.objects.create(
            title='First product',
            price=1,
            articul=articul,
            supplier=supplier1, is_available=True)

        product2 = Product.objects.create(title='Second product', price=1, articul=articul,
                supplier=supplier2, is_available=True)

        with self.assertRaises(IntegrityError):
            product3 = Product.objects.create(title='Third product', price=1, articul=articul,
                supplier=supplier1, is_available=True)
        
        with self.assertRaises(IntegrityError):
            product4 = Product.objects.create(title='Forth product', price=1, articul=articul,
                    supplier=supplier2, is_available=True)


class ProductManagerTest(TestCase):
    fixtures = ['test_data', ]

    # def test_supplier_own_articuls_pk_list(self):
    #     supplier = Supplier.objects.all().first()
    #     supplier_articuls_pk = supplier.own_articuls_pk_list
    #     self.assertIsInstance(supplier_articuls_pk, list)
    #     self.assertNotEqual(len(supplier_articuls_pk), 0)

    # def test_supplier_own_articuls_pk_list_empty(self):
    #     supplier = create_supplier()
    #     supplier_articuls_pk = supplier.own_articuls_pk_list
    #     self.assertIsInstance(supplier_articuls_pk, list)
    #     self.assertEqual(len(supplier_articuls_pk), 0)

    def test_compare(self):
        settings.DEBUG = True        

        supplier = Supplier.objects.all().first()
        supplier_articuls = supplier.own_articuls_queryset
        # supplier_products = supplier.own_articuls_pk_list[1]
        supplier_products = Product.objects.filter(supplier=supplier)

        print(len(connection.queries))

        articuls = supplier_articuls.prefetch_related('products')
        # print(articuls)

        for articul, product in zip(articuls, supplier_products):
            print(supplier)
            # print(articul.products.all().values_list('supplier'))
            print(articul.products.all())
            print(articul, product)
            # print(list(articul.products.all()))
            print(list(articul.products.all()).index(product))
            print('____________________________')


        print(len(connection.queries))
        settings.DEBUG = False
