# -*- coding: utf-8 -*-
from mixer.backend.django import mixer

from product.models import Product, Supplier


def create_supplier():
    user = mixer.blend('auth.user')
    return Supplier.objects.create(user=user)