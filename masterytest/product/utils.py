# -*- coding: utf-8 -*-
import random

from django.conf import settings

from mixer.backend.django import mixer

from product.models import Product, Supplier, Articul, Customer, ProductImage


def is_user_a_supplier(user):
    if user.is_authenticated() and Supplier.objects.filter(user=user):
        return True
    return False


def is_user_a_customer(user):
    if user.is_authenticated() and Customer.objects.filter(user=user):
        return True
    return False


def create_fixtures():
    Supplier.objects.bulk_create([Supplier(user=mixer.blend('auth.user')) for i in range(4)])
    Articul.objects.bulk_create(
        Articul(title=title) for title in ['one','two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
        )
    products = list()
    for supplier in Supplier.objects.all():
        for articul in Articul.objects.all():
            title = 'Product {} {}'.format(articul, supplier.user.username)
            price = random.randint(10, 100)
            is_av = random.choice([True, False])
            products.append(Product(title=title, price=price, articul=articul,
             is_available=is_av, supplier=supplier))

    Product.objects.bulk_create(products)


IMAGE_PATH = settings.BASE_DIR + '/product/img.jpg'

def create_product_images(product):
    for i in range(1,3):
        image = ProductImage.objects.create(product=product)
        file = open(IMAGE_PATH, 'rb')
        image.image.save('img.jpg', file)
    featured = ProductImage.objects.filter(product=product).first()
    featured.featured = True
    featured.save()
