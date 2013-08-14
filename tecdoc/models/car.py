# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)


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
    YESNO = (('0', u'Нет'),
             ('1', u'Да'),
            )

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

    for_car = models.SmallIntegerField(u'Для легковых',
                                       db_column='MOD_PC',
                                       choices=YESNO,
                                       blank=True, null=True)

    for_truck = models.SmallIntegerField(u'Для грузовых',
                                         db_column='MOD_CV',
                                         choices=YESNO,
                                         blank=True, null=True)

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
                                           .filter(model__designation__lang=tdsettings.LANG_ID,
                                                   full_designation__lang=tdsettings.LANG_ID)
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
    eng_volume = models.IntegerField(u'Объём двигателя (куб.см)',
                                     db_column='TYP_CCM',
                                     blank=True, null=True)
    cylinders = models.IntegerField(u'Количество цилиндров',
                                    db_column='TYP_CYLINDERS',
                                    blank=True, null=True)
    power_kw_from = models.IntegerField(u'Мощность двигателя (кВт): ОТ',
                                        db_column='TYP_KW_FROM',
                                        blank=True, null=True)
    power_kw_upto = models.IntegerField(u'Мощность двигателя (кВт): До',
                                        db_column='TYP_KW_UPTO',
                                        blank=True, null=True)
    power_hp_from = models.IntegerField(u'Мощность двигателя (л.с.): ОТ',
                                        db_column='TYP_HP_FROM',
                                        blank=True, null=True)
    power_hp_upto = models.IntegerField(u'Мощность двигателя (л.с.): До',
                                        db_column='TYP_HP_UPTO',
                                        blank=True, null=True)

    objects = CarTypeManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'TYPES'
        ordering = ['sorting', 'production_start']

    def __unicode__(self):
        return u'%s (%s-%s)' % (self.full_designation,
                                self.production_start, self.production_end or u'н.д.'
                               )

    def list_categories(self, parent=0):
        from tecdoc.models.category import CarSection
        filters = {'groups__parttypegroupsupplier__car_type': self}
        if parent != 0:
            filters['parent'] = parent
        return CarSection.objects.filter(**filters).distinct()

    def list_parts(self):
        from tecdoc.models.part import Part
        return Part.objects.filter(partgroup__parttypegroupsupplier__car_type=self).distinct()


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

