# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tecdoc.models import (Manufacturer, CarModel, CarType,
                           RootSection, CarSection, Part)

from pwshop.utils import paginate


def category_tree(request, parent=None):
    if parent is None:
        parent = RootSection()
    else:
        parent = CarSection.objects.get(id=parent)
    children = parent.get_children()

    parts = parent.get_parts()

    return TemplateResponse(request, 'tecdoc/category_tree.html',
                            {'cat': parent,
                             'children': children,
                             'parts': parts,
                            }
                            )


def category_tree_by_type(request, type_id, parent=None):
    types = CarType.objects.filter(model=model_id)
    return TemplateResponse(request, 'tecdoc/cartypes.html',
                            {'types': types,
                             'model': model}
                            )
