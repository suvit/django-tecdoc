# -*- coding: utf-8 -

from base import (TecdocModel, TecdocManager,
                  TecdocManagerWithDes)


class CarModelManager(TecdocManagerWithDes):

    def get_models(self, manufacturer, date_min=None, date_max=None,
                   search_text=None):

        query = self.get_query_set()
        query = query.select_related('manufacturer', 'designation__description').filter(manufacturer=manufacturer)

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

    manufacturer = models.ForeignKey(Manufacturer,
                                     verbose_name=u'Производитель',
                                     db_column='MOD_MFA_ID')

    designation = models.ForeignKey(CountryDesignation,
                                    verbose_name=u'Обозначение',
                                    db_column='MOD_CDS_ID')

    objects = CarModelManager()

    def __unicode__(self):
        return u'%s %s (%s-%s)' % (self.manufacturer,
                                       self.designation,
                                       self.production_start, self.production_end)

    class Meta:
        db_table = 'MODELS'


class Engine(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ENG_ID')

    manufacturer = models.ForeignKey(Manufacturer,
                                     verbose_name=u'Производитель',
                                     db_column='ENG_MFA_ID')

    code = models.CharField(u'Код', max_length=180, db_column='ENG_CODE')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='ENG_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='ENG_PCON_END')

    class Meta:
        db_table = 'ENGINES'


class CarType(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TYP_ID')

    designation = models.ForeignKey(CountryDesignation,
                                    verbose_name=u'Обозначение',
                                    db_column='TYP_CDS_ID')

    model = models.ForeignKey(CarModel,
                              verbose_name=u'Модель',
                              db_column='TYP_MOD_ID')

    sorting = models.IntegerField(u'Порядок', db_column='TYP_SORT')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='TYP_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='TYP_PCON_END')

    engines = models.ManyToManyField(Engine, verbose_name=u'Двигатели',
                                     through='tecdoc.CarTypeEngine')

    objects = TecdocManagerWithDes()

    class Meta:
        db_table = 'TYPES'
        ordering = ['sorting', 'production_start']

    def __unicode__(self):
        return u'(%s)%s %s (%s-%s)' % (self.id, self.model,
                                       self.designation,
                                       self.production_start, self.production_end
                                      )


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

    class Meta:
        db_table = 'LINK_TYP_ENG'

