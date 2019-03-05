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

from .decorators import supplier_required, is_user_a_supplier
from .models import Product, Supplier


class IndexView(TemplateView):
    template_name = "index.html"


class IsUserSupplierMixin(UserPassesTestMixin):
    def test_func(self):
        return is_user_a_supplier(self.request.user)

class IsUserSupplierMixin2(AccessMixin):
    permission_denied_message = 'OOpa'
    raise_exception = True

    def dispatch(self, request, *args, **kwargs):
        if not is_user_a_supplier(request.user):
            return self.handle_no_permission()
        return super(IsUserSupplierMixin2, self).dispatch(request, *args, **kwargs)


@method_decorator([login_required, supplier_required], name='dispatch')
class SupplierRegularView(TemplateView):
    template_name = 'supplier_product_list.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierRegularView, self).get_context_data(**kwargs)
        supplier = self.request.user.supplier
        context['products'] = supplier.get_own_products
        return context


# @method_decorator([login_required, supplier_required], name='dispatch')
class SupplierComparativeView(TemplateView):
    template_name = 'supplier_product_list_comparative.html'

    def get_context_data(self, **kwargs):
        context = super(SupplierRegularView, self).get_context_data(**kwargs)
        supplier = self.request.user.supplier
        context['products_with_comparative_list'] = supplier.get_own_products_with_comparative_list
        return context


def test_data_view(request):
    # Products.objects.all()
    user = User.objects.create_user(username='testuser2', password='qwerty123')
    Supplier.objects.create(user=user)
    return HttpResponse(user)