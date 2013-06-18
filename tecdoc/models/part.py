# -*- coding: utf-8 -
from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes, Designation)


class PartManager(TecdocManagerWithDes):
    def get_query_set(self, *args, **kwargs):
        query = super(PartManager, self).get_query_set(*args, **kwargs)
        query = query.select_related('designation__description',
                                     'supplier')

        query = query.prefetch_related('lookup', 'images')
        return query


class Part(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ART_ID')

    title = models.CharField(u'Название', max_length=66,
                             db_column='ART_ARTICLE_NR')

    supplier = models.ForeignKey('tecdoc.Supplier', verbose_name=u'Поставщик',
                                 db_column='ART_SUP_ID')

    # don`t use
    #short_designation = models.ForeignKey('tecdoc.Designation',
    #                                      verbose_name=u'Краткое Обозначение',
    #                                      db_column='ART_DES_ID',
    #                                      related_name='parts_with_short_designation')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='ART_COMPLETE_DES_ID')
                                    
    car_types = models.ManyToManyField('tecdoc.CarType',
                                       verbose_name=u'Модификации авто',
                                       through='tecdoc.PartTypeGroupSupplier',
                                       related_name='parts')

    groups = models.ManyToManyField('tecdoc.Group',
                                    verbose_name=u'Группа запчастей',
                                    through='tecdoc.PartGroup',
                                    related_name='parts')

    criteries = models.ManyToManyField('tecdoc.Criteria',
                                      verbose_name=u'Оговорки',
                                      through='tecdoc.PartCriteria',
                                      related_name='parts')

    texts = models.ManyToManyField('tecdoc.TextLanguage',
                                    verbose_name=u'Описание',
                                    through='tecdoc.PartDescription',
                                    related_name='parts')

    images = models.ManyToManyField('tecdoc.Image',
                                    verbose_name=u'Изображения',
                                    through='tecdoc.PartImage',
                                    related_name='parts')

    #pdfs = models.ManyToManyField('tecdoc.PdfFile',
    #                              verbose_name=u'Инструкция',
    #                              through='tecdoc.PartImage',
    #                              related_name='parts') 

    objects = PartManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ARTICLES'

    def __unicode__(self):
        return u'%s %s %s' % (self.designation,
                                      self.supplier,
                                      self.title)

    def get_manufacturer(self):
        return u' '.join(unicode(part.kind == 4 and self.lookup.manufacturer or self.supplier) for part in self.lookup.all())

    def get_title(self):
        return u' '.join(unicode(part.kind in [2,3] and self.lookup.number or self.title) for part in self.lookup.all())


class GroupManager(TecdocManagerWithDes):
    def get_query_set(self, *args, **kwargs):
        query = super(GroupManager, self).get_query_set(*args, **kwargs)
        query = query.filter(standard__lang=tdsettings.LANG_ID,
                             assembly__lang=tdsettings.LANG_ID,
                             intended__lang=tdsettings.LANG_ID)
        return query.select_related('designation__description',
                                    'standard__description',
                                    'assembly__description',
                                    'intended__description')

class Group(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GA_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='GA_DES_ID')

    standard = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Стандарт',
                                 db_column='GA_DES_ID_STANDARD',
                                 related_name='+')

    assembly = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Где устанавливается',
                                 db_column='GA_DES_ID_ASSEMBLY',
                                 related_name='+')

    intended = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Во что входит',
                                 db_column='GA_DES_ID_INTENDED',
                                 related_name='+')

    sections = models.ManyToManyField('tecdoc.CarSection',
                                      verbose_name=u'Категории',
                                      through='tecdoc.SectionGroup',
                                      related_name='groups')

    objects = GroupManager()

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'GENERIC_ARTICLES'

    def full_title(self):
        return u'%s - %s - %s - %s' % (self.designation,
                                 self.standard,
                                 self.assembly,
                                 self.intended)
    def __unicode__(self):
        return unicode(self.designation)

class PartDescription(TecdocModel):

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='AIN_ART_ID')

    group = models.ForeignKey(Group, verbose_name=u'Группа запчастей',
                              db_column='AIN_GA_ID')

    text = models.ForeignKey('tecdoc.TextLanguage',
                             verbose_name=u'Обозначение',
                             db_column='AIN_TMO_ID')

    class Meta(TecdocModel.Meta):
        db_table= tdsettings.DB_PREFIX + 'ARTICLE_INFO'


class SectionGroup(TecdocModel):
    car_section = models.ForeignKey('tecdoc.CarSection',
                                    verbose_name=u'Категория',
                                    db_column='LGS_STR_ID')

    group = models.ForeignKey(Group,
                              verbose_name=u'Группа запчатей',
                              db_column='LGS_GA_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_GA_STR'


class PartGroup(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LA_ID')

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LA_ART_ID')

    group = models.ForeignKey(Group,
                              verbose_name=u'Группа запчастей',
                              db_column='LA_GA_ID')

    sorting = models.IntegerField(u'Порядок', db_column='LA_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_ART'


class PartGroupSupplier(TecdocModel):
    # part and group primary key
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LAG_ART_ID')

    group = models.ForeignKey(Group, verbose_name=u'Группа запчастей',
                              db_column='LAG_GA_ID')

    supplier = models.ForeignKey('tecdoc.Supplier',
                                 verbose_name=u'Поставщик',
                                 db_column='LAG_SUP_ID')

    class Meta:
        db_table = tdsettings.DB_PREFIX + 'LINK_ART_GA'


class PartTypeGroupSupplier(TecdocModel):
    # car_type, part, group and sort are primary key
    car_type = models.ForeignKey('tecdoc.CarType',
                                 verbose_name=u'Модификация модели',
                                 db_column='LAT_TYP_ID')

    # XXX needed to PartGroup
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LAT_LA_ID')

    group = models.ForeignKey(Group, verbose_name=u'Группа Запчастей',
                              db_column='LAT_GA_ID')

    supplier = models.ForeignKey('tecdoc.Supplier', verbose_name=u'Поставщик',
                                 db_column='LAT_SUP_ID')

    sorting = models.IntegerField(u'Порядок', db_column='LAT_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_LA_TYP'


class PartLookup(TecdocModel):
    KIND = ((1, u'не оригинал'),
            (2, u'торговый'),
            (3, u'оригинал'),
            (4, u'не оригинал'),
            (5, u'не оригинал'),
           )

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                                primary_key=True,
                                db_column='ARL_ART_ID',
                                related_name='lookup')

    number = models.CharField(u'Номер', max_length=105,
                              db_column='ARL_DISPLAY_NR',
                             )

    # derived from number
    search_number = models.CharField(u'Номер для поиска', max_length=105,
                                     db_column='ARL_SEARCH_NUMBER',
                                     )

    kind = models.IntegerField('Тип', choices=KIND,
                               db_column='ARL_KIND')

    brand = models.ForeignKey('tecdoc.Brand',
                              verbose_name=u'Производитель',
                              db_column='ARL_BRA_ID')

    sorting = models.IntegerField(u'Порядок', db_column='ARL_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ART_LOOKUP'


class PartList(TecdocModel):
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='ALI_ART_ID')

    inner_part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                                   db_column='ALI_ART_ID_COMPONENT',
                                   related_name='inner_parts')

    group = models.ForeignKey(Group, verbose_name=u'Группа Запчастей',
                              db_column='ALI_GA_ID')

    quantity = models.IntegerField(u'Количество',
                                   db_column='ALI_QUANTITY')

    sorting = models.IntegerField(u'Порядок', db_column='ALI_SORT')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ARTICLE_LISTS'


#TODO
class PartListCriteria(TecdocModel):
    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ARTICLE_LIST_CRITERIA'


class CountryProperty(TecdocModel):
    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='ACS_ART_ID',
                             related_name='properties')

    pack = models.ForeignKey('tecdoc.Designation', verbose_name=u'Упаковка',
                             db_column='ACS_PACK_UNIT',
                             related_name='+')

    quantity = models.ForeignKey('tecdoc.Designation',
                                 verbose_name=u'Количество',
                                 db_column='ACS_QUANTITY_PER_UNIT',
                                 related_name='+')

    status = models.ForeignKey('tecdoc.Designation',
                               verbose_name=u'Статус',
                               db_column='ACS_KV_STATUS_DES_ID',
                               related_name='+')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'ART_COUNTRY_SPECIFICS'
