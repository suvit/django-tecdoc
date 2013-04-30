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

def search_view(request, query):
    form = SearchForm({'query': query})
    if form.is_valid():
        parts = Part.objects.lookup(query=form.cleaned_data['query'])
    else:
        parts = None
        messages.add_message()

    return TemplateResponse(request, 'tecdoc/search_part.html',
                            {'form': form,
                             'parts': parts})
