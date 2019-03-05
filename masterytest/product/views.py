# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.http import HttpResponse

from .utils import is_user_a_supplier, is_user_a_customer
from .models import Product, Supplier


class IndexView(TemplateView):
    template_name = "index.html"


class IsUserSupplierMixin(AccessMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not is_user_a_supplier(request.user):
            return self.handle_no_permission()
        return super(IsUserSupplierMixin, self).dispatch(request, *args, **kwargs)


class SupplierRegularView(IsUserSupplierMixin, TemplateView):
    template_name = 'supplier_product_list.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierRegularView, self).get_context_data(**kwargs)
        supplier = self.request.user.supplier
        context['products'] = supplier.get_own_products
        return context


class SupplierComparativeView(IsUserSupplierMixin, TemplateView):
    template_name = 'supplier_product_list_comparative.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierComparativeView, self).get_context_data(**kwargs)
        supplier = self.request.user.supplier
        context['products_with_comparative_list'] = supplier.get_own_products_with_comparative_list
        return context


class IsUserCustomerMixin(AccessMixin):
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not is_user_a_customer(request.user):
            return self.handle_no_permission()
        return super(IsUserCustomerMixin, self).dispatch(request, *args, **kwargs)


class CustomerView(IsUserCustomerMixin, TemplateView):
    template_name = 'customer.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context


def test_data_view(request):
    # Products.objects.all()
    user = User.objects.create_user(username='testuser2', password='qwerty123')
    Supplier.objects.create(user=user)
    return HttpResponse(user)