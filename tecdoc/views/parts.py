# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from django.template.response import TemplateResponse

from tecdoc.models import Part


class PartView(DetailView):
    model = Part
    pk_url_kwarg = 'part_id'

    template_name = 'tecdoc/part.html'


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
