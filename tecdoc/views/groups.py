# -*- coding: utf-8 -*-
from django.views.generic import DetailView

from tecdoc.models import Group


class GroupView(DetailView):
    model = Group
    pk_url_kwarg = 'group_id'

    template_name = 'tecdoc/group.html'
