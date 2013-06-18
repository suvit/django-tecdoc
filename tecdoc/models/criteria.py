# -*- coding: utf-8 -
from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)


class Criteria(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='CRI_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='CRI_DES_ID')

    short_designation = models.ForeignKey('tecdoc.Designation',
                                          verbose_name=u'Краткое Обозначение',
                                          db_column='CRI_SHORT_DES_ID',
                                          related_name='+')

    unit = models.ForeignKey('tecdoc.Designation',
                             verbose_name=u'Упаковка',
                             db_column='CRI_UNIT_DES_ID',
                             related_name='+')

    type = models.CharField(u'Тип', max_length=1,
                            db_column='CRI_TYPE')

    is_interval = models.BooleanField(u'Интервальный',
                                      db_column='CRI_IS_INTERVAL')

    child = models.ForeignKey('self', verbose_name=u'Второй критерий',
                              db_column='CRI_SUCCESSOR',
                              related_name='parents')

    objects = TecdocManagerWithDes()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'CRITERIA'

    def __unicode__(self):
        return u'%s %s %s %s' % (self.type, 
                                 self.designation or self.short_designation,
                                 self.get_unit(),
                                 self.is_interval and u'Интервальный' or '')

    def get_unit(self):
        return self.unit if self.unit_id else ''


class PartCriteria(TecdocModel):
    part = models.ForeignKey('tecdoc.Part', verbose_name=u'Запчасть',
                             db_column='ACR_ART_ID')

    group = models.ForeignKey('tecdoc.Group', verbose_name=u'Группа Запчастей',
                              db_column='ACR_GA_ID')

    criteria = models.ForeignKey(Criteria, verbose_name=u'Запчасть',
                                 db_column='ACR_CRI_ID')

    value = models.CharField(u'Значение', max_length=60,
                             db_column='ACR_VALUE')

    description = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Описание',
                                    db_column='ACR_KV_DES_ID')

    sorting = models.IntegerField(u'Порядок', db_column='ACR_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ARTICLE_CRITERIA'

    def get_value(self):
        return self.value or self.description
