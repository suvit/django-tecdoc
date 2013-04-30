# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse


from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate


def cartypes(request, model_id):
    model = get_object_or_404(CarModel, id=model_id)
    return TemplateResponse(request, 'tecdoc/cartypes.html',
                            {'model': model}
                            )

def car_type(request, car_type_id):
    car_type = get_object_or_404(CarType, id=car_type_id)
    return TemplateResponse(request, 'tecdoc/cartype.html',
                            {'car_type': car_type}
                           )
