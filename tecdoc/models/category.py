# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes, Designation)

from tecdoc.models.part import Part, Group


class RootSection(object):
    id = None
    level = 0

    def __unicode__(self):
        return u'Корень'

    def get_parts(self):
        return Part.objects.all()

    def get_groups(self):
        return Group.objects.all()

    def get_children(self):
        return CarSection.objects.filter(parent__isnull=True)

    def has_children(self):
        return True

    def get_ancestors(self):
        return CarSection.objects.none()


class CarSection(TecdocModel):
    # TODO use mptt here
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='STR_ID')

    parent = models.ForeignKey('self', db_column='STR_ID_PARENT',
                               related_name='children')

    type = models.IntegerField(u'Тип',
                               db_column='STR_TYPE')

    level = models.IntegerField(u'Уровень дерева',
                                db_column='STR_LEVEL')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='STR_DES_ID')

    def __unicode__(self):
        return u'%s' % (self.designation)

    objects = TecdocManagerWithDes()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'SEARCH_TREE'

    def get_children(self):
        return self.children.all()

    def has_children(self):
        return self.children.exists()

    def get_ancestors(self):
        if self.parent is None:
            return CarSection.objects.none()

        parents = list()
        parent = self
        while parent.parent_id is not None:
             parents.insert(0, parent.parent_id)
             parent = parent.parent

        return CarSection.objects.filter(id__in=parents).order_by('level')

    def get_parts(self, car_type=None):
        return Part.objects.filter(groups__sections=self).distinct()

    def get_groups(self):
        return Group.objects.filter(sections=self)

    """
    def lookup_by_number(self, manufacturers=None):
        query = Part.objects.filter(lookup=self)

        if manufacturers:
            query = query.filter(lookup_manufacturer=manufacturers)

        query.select_related('lookup__manufacturer',
                             'designation__description')

        return query

    def lookup_analog(self, part_id, part_type=None):
        query = Part.objects.filter(lookup__part=part_id)

        if part_type:
            query.filter(lookup__kind=part_type)

        return query

    def get_part_info(self, part_id):
        query = Part.objects.filter(id=part_id)

        query = query.select_related('properties',
                                     'texts')

    def get_properties(self, part_id):
        query = Part.objects.filter(id=part_id)

        query = query.select_related('criteries')
    """
