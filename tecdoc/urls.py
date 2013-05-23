from django.conf.urls.defaults import *
from django.conf import settings

from tecdoc.views.manufacturer import ManufacturerList, ManufacturerView
from tecdoc.views.cartype import CarTypeView, CarModelView 

urlpatterns = patterns("tecdoc.views",
    url(r'^manufacturers/$', ManufacturerList.as_view(),
        name='tecdoc-manufacturers'),
    url(r'^manufacturer/(?P<mnf_id>\d+)/$', ManufacturerView.as_view(),
        name='tecdoc-manufacturer'),
    url(r'^models/(?P<model_id>\d+)/$', CarModelView.as_view(),
        name='tecdoc-models'),

    url(r'^suppliers/$', 'suppliers.suppliers',
        name='suppliers'),
    url(r'^suppliers/(?P<supplier_id>\d+)/$', 'suppliers.supplier_view',
        name='supplier'),

    url(r'^car_types/(?P<car_type_id>\d+)/$', CarTypeView.as_view(),
        name='car_type'),

    url(r'^categories/$', 'category.category_tree',
        name='category_tree'),
    url(r'^categories/(?P<parent>\d+)/$$', 'category.category_tree',
        name='category_tree'),

    url(r'^cartypes/(?P<type_id>\d+)/category/$',
        'category.category_tree_by_type',
        name='caregory_tree_by_type'),
    url(r'^cartypes/(?P<type_id>\d+)/category/(?P<parent>\d+)$',
        'category.category_tree_by_type',
        name='caregory_tree_by_type'),

    url(r'^groups/(?P<group_id>\d+)/$',
        'groups.group_view',
        name='group'),

    url(r'^parts/(?P<part_id>\d+)/$',
        'parts.part_view',
        name='part'),
)
