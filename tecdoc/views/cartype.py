# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from django.views.generic import ListView, DetailView



from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate


class CarTypeView(DetailView):
    model = CarType
    template_name = 'tecdoc/cartype.html'
    pk_url_kwarg = 'car_type_id'


class CarModelView(DetailView):
    model = CarModel

    template_name = 'tecdoc/cartypes.html'
    pk_url_kwarg = 'model_id'
