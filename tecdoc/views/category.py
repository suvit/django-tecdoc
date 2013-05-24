# -*- coding: utf-8 -*-
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)


def category_tree(request, parent=None):
    if parent is None:
        parent = RootSection()
    else:
        parent = get_object_or_404(CarSection, id=parent)

    return TemplateResponse(request, 'tecdoc/categories.html',
                            {'cat': parent,
                            }
                            )


def category_tree_by_type(request, type_id, parent=None):
    types = CarType.objects.filter(model=model_id)
    return TemplateResponse(request, 'tecdoc/cartypes.html',
                            {'types': types,
                             'model': model}
                            )
