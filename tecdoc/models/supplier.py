# -*- coding: utf-8 -

from django.db import models
from django.db.models.base import ModelBase

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)

class Supplier(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='SUP_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='SUP_BRAND',
                             blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'SUPPLIERS'

    def __unicode__(self):
        return self.title.capitalize()

    def get_country(self):
        return self.addresses.filter(type=1,
                                     country_flag=0).get().country_postal


class SupplierLogo(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='SLO_ID')

    supplier = models.ForeignKey('tecdoc.Supplier',
                                 verbose_name=u'Поставщик',
                                 db_column='SLO_SUP_ID')

    language = models.ForeignKey('tecdoc.Language',
                                 verbose_name=u'Язык',
                                 db_column='SLO_LNG_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'SUPPLIER_LOGOS'


class SupplierAddress(TecdocModel):
    # XXX not a primary key
    supplier = models.ForeignKey('tecdoc.Supplier', primary_key=True,
                                 verbose_name=u'Поставщик',
                                 db_column='SAD_SUP_ID',
                                 related_name='addresses')

    type = models.IntegerField(u'Тип',
                               db_column='SAD_TYPE_OF_ADDRESS')

    # needed with value 0
    country_flag = models.IntegerField(u'Страна',
                                       db_column='SAD_COU_ID')

    country_postal = models.ForeignKey('tecdoc.Country',
                                       verbose_name=u'Почтовый адресс. Страна',
                                       db_column='SAD_COU_ID_POSTAL',
                                       related_name="addresses")

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'SUPPLIER_ADDRESSES'

