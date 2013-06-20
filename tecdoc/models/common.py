# -*- coding: utf-8 -

from django.db import models

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
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


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
        verbose_name = u'Бренд'
        verbose_name_plural = u'Бренды'

    def __unicode__(self):
        return self.title.capitalize()


class Manufacturer(TecdocModel):

    YESNO = (('0', u'Нет'),
             ('1', u'Да'),
            )

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MFA_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='MFA_BRAND',
                             blank=True, null=True)

    code = models.CharField(u'Код', max_length=30,
                             db_column='MFA_MFC_CODE',
                             blank=True, null=True)

    for_car = models.SmallIntegerField(u'Для легковых',
                                       db_column='MFA_PC_MFC',
                                       choices=YESNO,
                                       blank=True, null=True)

    for_truck = models.SmallIntegerField(u'Для грузовых',
                                        db_column='MFA_CV_MFC',
                                        choices=YESNO,
                                        blank=True, null=True)

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'MANUFACTURERS'
        ordering = ['title']
        verbose_name = u'Производитель автомобилей'
        verbose_name_plural = u'Производители автомобилей'

    __unicode__ = Brand.__unicode__.im_func
