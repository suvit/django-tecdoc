# -*- coding: utf-8 -

from django.db import models
from django.db.models.base import ModelBase

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)


class Country(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='COU_ID')

    iso_code = models.CharField(u'Код ISO2', max_length=6,
                                db_column='COU_ISO2',
                                blank=True, null=True)

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='COU_DES_ID')

    currency_code = models.CharField(u'Код Валюты', max_length=9,
                                     db_column='COU_CURRENCY_CODE',
                                     blank=True, null=True)

    objects = TecdocManagerWithDes()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'COUNTRIES'


class Brand(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='BRA_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='BRA_BRAND',
                             blank=True, null=True)

    code = models.CharField(u'Название', max_length=30,
                             db_column='BRA_MFC_CODE',
                             blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'BRANDS'
        ordering = ['title']


class Manufacturer(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MFA_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='MFA_BRAND',
                             blank=True, null=True)

    code = models.CharField(u'Название', max_length=30,
                             db_column='MFA_MFC_CODE',
                             blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'MANUFACTURERS'
        ordering = ['title']

    def __unicode__(self):
        return self.title.capitalize()


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

