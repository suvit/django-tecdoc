# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from tecdoc.models import CarModel, CarType


class CarTypeView(DetailView):
    model = CarType
    template_name = 'tecdoc/cartype.html'
    pk_url_kwarg = 'car_type_id'


class CarModelView(DetailView):
    model = CarModel

    template_name = 'tecdoc/cartypes.html'
    pk_url_kwarg = 'model_id'
