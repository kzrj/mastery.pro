# -*- coding: utf-8 -*-
import random

from mixer.backend.django import mixer

from product.models import Product, Supplier


def create_fixtures():
    Supplier.objects.bulk_create([Supplier(user=mixer.blend('auth.user')) for i in range(4)])
    articuls = ['one','two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
    products = list()

    for supplier in Supplier.objects.all():
        for articul in articuls:
            title = 'Product {} {}'.format(articul, supplier.user.username)
            price = random.randint(10, 100)
            is_av = random.choice([True, False])
            products.append(Product(title=title, price=price, articul=articul,
             is_available=is_av, supplier=supplier))

    Product.objects.bulk_create(products)