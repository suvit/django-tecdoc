# -*- coding: utf-8 -*-
# Create your views here.
from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from tecdoc.models import Group

from pwshop.utils import paginate

def group_view(request, group_id):

    group = Group.objects.prefetch_related('sections',
                                          ).get(id=group_id)

    return TemplateResponse(request, 'tecdoc/group.html',
                            {'group': group,
                            }
                           )

