# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate


def cartypes(request, model_id):
    model = CarModel.objects.get(id=model_id)
    types = CarType.objects.filter(model=model_id)
    return TemplateResponse(request, 'tecdoc/cartypes.html',
                            {'types': types,
                             'model': model}
                            )

def car_type(request, car_type_id):
    car_type = CarType.objects.get(id=model_id)
    return TemplateResponse(request, 'tecdoc/cartype.html',
                            {'car_type': car_type}
                           )
