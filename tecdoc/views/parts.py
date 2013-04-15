# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate

def part_view(request, part_id):

    part = Part.objects.prefetch_related('groups',
                                         'criteries',
                                         'car_types',
                                        ).get(id=part_id)

    return TemplateResponse(request, 'tecdoc/part.html',
                            {'part': part,
                            }
                           )

