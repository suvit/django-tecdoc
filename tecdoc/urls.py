from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns("tecdoc.views",
    url(r'^manufacturers/$', 'manufacturer.mfa',
        name='manufacturers'),
    url(r'^manufacturer/(?P<mnf_id>\d+)/$', 'manufacturer.models',
        name='manufacturer'),
    url(r'^models/(?P<model_id>\d+)/$', 'cartype.cartypes',
        name='models'),

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
)
