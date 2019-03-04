# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    @property
    def own_articuls_pk_list(self):
        products = Product.objects.filter(supplier=self).values_list('articul')
        supplier_articuls_pk = [ a[0] for a in products ]
        return supplier_articuls_pk, products

    @property
    def own_articuls_queryset(self):
        return Articul.objects.filter(pk__in=self.own_articuls_pk_list[0])


# class ArticulManager(models.Manager):
#     def products_sorted_by_price(self):
#         return self.model.products.all().order_by('-price')


@python_2_unicode_compatible
class Articul(models.Model):
    title = models.CharField(max_length=10)

    # objects = ArticulManager()

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.product.title + 'image %d' % self.pk
