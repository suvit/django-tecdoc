# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)

from tecdoc.models.category import CarSection


class CarModelManager(TecdocManagerWithDes):

    def get_query_set(self, *args, **kwargs):
        return (super(CarModelManager, self).get_query_set(*args, **kwargs)
                                            .select_related('manufacturer',
                                                            'designation__description')
               )

    def get_models(self, manufacturer, date_min=None, date_max=None,
                   search_text=None):

        query = self.filter(manufacturer=manufacturer)

        if date_min:
             # TODO
             pass

        if date_max:
             pass

        if search_text:
             query.filter(designation__description__text__icontains=search_text)

        return query


class CarModel(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MOD_ID')
    production_start = models.IntegerField(u'Начало производства',
                                        db_column='MOD_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='MOD_PCON_END')

    manufacturer = models.ForeignKey('tecdoc.Manufacturer',
                                     verbose_name=u'Производитель',
                                     db_column='MOD_MFA_ID')

    designation = models.ForeignKey('tecdoc.CountryDesignation',
                                    verbose_name=u'Обозначение',
                                    db_column='MOD_CDS_ID')

    objects = CarModelManager()

    def __unicode__(self):
        return u'%s %s (%s-%s)' % (self.manufacturer,
                                   self.designation,
                                   self.production_start, self.production_end or u'н.д.')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'MODELS'


class Engine(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ENG_ID')

    manufacturer = models.ForeignKey('tecdoc.Manufacturer',
                                     verbose_name=u'Производитель',
                                     db_column='ENG_MFA_ID')

    code = models.CharField(u'Код', max_length=180, db_column='ENG_CODE')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='ENG_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='ENG_PCON_END')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ENGINES'


class CarTypeManager(TecdocManagerWithDes):

    def get_query_set(self, *args, **kwargs):
        return (super(CarTypeManager, self).get_query_set(*args, **kwargs)
                                           .filter(model__designation__lang=16,
                                                   full_designation__lang=16)
                                           .select_related('model__manufacturer',
                                                           'model__designation__description',
                                                           'full_designation__description',
                                                           'designation__description')
               )


class CarType(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TYP_ID')

    designation = models.ForeignKey('tecdoc.CountryDesignation',
                                    verbose_name=u'Обозначение',
                                    db_column='TYP_CDS_ID')

    full_designation = models.ForeignKey('tecdoc.CountryDesignation',
                                         verbose_name=u'Полное обозначение',
                                         db_column='TYP_MMT_CDS_ID',
                                         related_name='+'
                                        )

    model = models.ForeignKey(CarModel,
                              verbose_name=u'Модель',
                              db_column='TYP_MOD_ID',
                              related_name='cartypes')

    sorting = models.IntegerField(u'Порядок', db_column='TYP_SORT')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='TYP_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='TYP_PCON_END')

    engines = models.ManyToManyField(Engine, verbose_name=u'Двигатели',
                                     through='tecdoc.CarTypeEngine',
                                     related_name='cartypes')

    objects = CarTypeManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'TYPES'
        ordering = ['sorting', 'production_start']

    def __unicode__(self):
        return u'%s (%s-%s)' % (self.full_designation,
                                self.production_start, self.production_end or u'н.д.'
                               )

    def list_categories(self, parent=10001):
        return CarSection.objects.filter(parent=parent,
                                         groups__parts__car_types=self).distinct()


class CarTypeEngine(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LTE_TYP_ID')

    car_type = models.ForeignKey(CarType,
                                 verbose_name=u'Модификация модели',
                                 db_column='LTE_NR')

    engine = models.ForeignKey(Engine,
                               verbose_name=u'Двигатель',
                               db_column='LTE_ENG_iD')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='LTE_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='LTE_PCON_END')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_TYP_ENG'

