# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Prefetch, Q
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@python_2_unicode_compatible
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def get_own_products(self):
        return Product.objects.filter(supplier=self).select_related('articul')

    def get_own_articuls(self, products):
        articul_pk_list = [p.articul.pk for p in products]
        return Articul.objects.filter(pk__in=articul_pk_list)

    def get_own_articuls_with_related_available_products(self, articuls):
        return articuls.prefetch_related(
            Prefetch(
                'products',
                queryset=Product.objects.filter((Q(is_available=True) | Q(supplier=self))),
                to_attr='available_products'
                )
            )
        
    @property
    def get_own_products_with_comparative_list(self):
        products_with_comparative_list = list()

        products = self.get_own_products
        articuls = self.get_own_articuls(products)
        articuls_with_products = self.get_own_articuls_with_related_available_products(articuls)

        for articul, product in zip(articuls_with_products, products):
            idx = articul.available_products.index(product)
            products_with_comparative_list.append({'product': product,
                'products_with_less_price': articul.available_products[:idx]})

        return products_with_comparative_list


@python_2_unicode_compatible
class Articul(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class ProductManager(models.Manager):
    def available_and_not_own(self, supplier):
        return self.model.objects.exclude(supplier=supplier).filter(is_available=True)


@python_2_unicode_compatible
class Product(models.Model):
    title = models.CharField(max_length=128, default='')
    price = models.IntegerField(default=0)
    articul = models.ForeignKey(Articul, on_delete=models.CASCADE, related_name='products')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products')
    is_available = models.BooleanField(default=False)

    objects = ProductManager()

    class Meta:
        unique_together = ("articul", "supplier")
        ordering = ['articul', 'price']

    def __str__(self):
        return self.title + ' ' + str(self.price)

    def products_with_same_articul_and_better_price(self):
        products = Product.objects.available_and_not_own(self.supplier).filter(articul=self.articul)
        return products.filter(price__lt=self.price)



@python_2_unicode_compatible
class ProductImage(models.Model):
    image = models.ImageField()
    featured = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        ordering = ['-featured',]

    def __str__(self):
        return self.product.title + 'image %d' % self.pk
