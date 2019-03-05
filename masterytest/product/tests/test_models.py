from mixer.backend.django import mixer

from django.test import TestCase, TransactionTestCase
from django.db.utils import IntegrityError
from django.db.models import Q
from django.db.models.query import QuerySet

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


class SupplierModelTest(TransactionTestCase):
    fixtures = ['test_data', ]

    def setUp(self):
        self.supplier = Supplier.objects.all().first()

    def test_get_own_products(self):
        with self.assertNumQueries(1):
            products_pk = [p.pk for p in self.supplier.get_own_products]

        regular_products_pk = [ p.pk for p in Product.objects.filter(supplier=self.supplier)]
        self.assertListEqual(products_pk, regular_products_pk)

    def test_get_own_articuls(self):
        products = self.supplier.get_own_products
        articuls = self.supplier.get_own_articuls(products)
        self.assertIsInstance(articuls, QuerySet)

        regular_articuls_pk = [a.pk for a in Articul.objects.filter(products__in=products)]
        articuls_pk = [a.pk for a in articuls]
        regular_articuls_pk.sort()
        articuls_pk.sort()
        self.assertListEqual(articuls_pk, regular_articuls_pk)

    def test_get_own_articuls_with_related_available_products(self):
        products = self.supplier.get_own_products
        articuls = self.supplier.get_own_articuls(products)
        
        with self.assertNumQueries(2):
            articuls_with_products = self.supplier.get_own_articuls_with_related_available_products(articuls)
            for articul in articuls_with_products:
                articul.available_products

        for articul in articuls_with_products:
            products = Product.objects.filter(articul=articul). \
                filter(Q(is_available=True) | Q(supplier=self.supplier))
            self.assertListEqual(articul.available_products, list(products))

    def test_get_own_products_with_comparative_list(self):
        products = self.supplier.get_own_products

        with self.assertNumQueries(3):
            products_with_comparative_list = self.supplier.get_own_products_with_comparative_list()
            len(products_with_comparative_list)

        for product_with_list, product in zip(products_with_comparative_list, products):
            self.assertEqual(product_with_list['product'], product)

            products_with_less_price = Product.objects \
                                        .filter(articul=product.articul) \
                                        .filter(is_available=True) \
                                        .filter(price__lt=product.price)
            self.assertListEqual(product_with_list['products_with_less_price'],
                 list(products_with_less_price))
