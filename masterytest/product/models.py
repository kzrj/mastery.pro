# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class ProductManager(models.Manager):
    def available_and_not_own(self, supplier):
        return self.model.objects.exclude(supplier=supplier).filter(is_available=True)


@python_2_unicode_compatible
class Product(models.Model):
    title = models.CharField(max_length=128, default='')
    price = models.IntegerField(default=0, null=True)
    articul = models.CharField(max_length=10)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, related_name='products')
    is_available = models.BooleanField(default=False)

    objects = ProductManager()

    class Meta:
        unique_together = ("articul", "supplier")
        ordering = ['articul', 'price']

    def __str__(self):
        return self.title

    def products_with_same_articul_and_better_price(self):
        products = Product.objects.available_and_not_own(self.supplier).filter(articul=self.articul)
        return products.filter(price__lt=self.price)



@python_2_unicode_compatible
class ProductImage(models.Model):
    image = models.ImageField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.product.title + 'image %d' % self.pk
