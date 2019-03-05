from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from .models import Supplier


def is_user_a_supplier(user):
    if user.is_authenticated() and Supplier.objects.filter(user=user):
        return True
    return False

def supplier_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        is_user_a_supplier,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator