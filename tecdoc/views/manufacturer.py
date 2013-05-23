# -*- coding: utf-8 -*-
# Create your views here.
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from tecdoc.models import Manufacturer, CarModel


class ManufacturerList(ListView):

    queryset = Manufacturer.objects.filter(carmodel__gt=0).distinct()

    template_name = 'tecdoc/manufacturers.html'


class ManufacturerView(DetailView):
    model = Manufacturer
    pk_url_kwarg = 'mnf_id'

    template_name = 'tecdoc/manufacturer.html'
