# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate

def mfa(request):
    mfa = Manufacturer.objects.filter(carmodel__gt=0).distinct()
    return TemplateResponse(request, 'tecdoc/manufacturers.html',
                            {'mfa':mfa}
                           )


def models(request, mnf_id):
    manufacturer = Manufacturer.objects.get(id=mnf_id)
    models = CarModel.objects.get_models(brand=mnf_id)
    return TemplateResponse(request, 'tecdoc/manufacturer.html',
                            {'models': models,
                             'manufacturer': manufacturer}
                           )
