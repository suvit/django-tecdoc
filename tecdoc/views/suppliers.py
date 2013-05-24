# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from tecdoc.models import Supplier


class SupplierList(ListView):
    model = Supplier
   
    template_name = 'tecdoc/suppliers.html'


class SupplierView(DetailView):
    model = Supplier

    pk_url_kwarg = 'supplier_id'

    template_name = 'tecdoc/supplier.html'