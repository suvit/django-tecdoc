# -*- coding: utf-8 -*-
# Create your views here.
from django.template.response import TemplateResponse

from tecdoc.models import (Supplier)

def suppliers(request):
    suppliers = Supplier.objects.all()
    return TemplateResponse(request, 'tecdoc/suppliers.html',
                            {'suppliers': suppliers}
                           )

def supplier_view(request, supplier_id):
    pass
