# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from tecdoc.models import Manufacturer


class ManufacturerList(ListView):
    queryset = Manufacturer.objects.filter(carmodel__gt=0).distinct()

    template_name = 'tecdoc/manufacturers.html'


class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    template_name = 'tecdoc/manufacturer.html'
