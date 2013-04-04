# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings


class TecdocManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManager, self).get_query_set(*args, **kwargs)
                                          .using('tecdoc')
                                          )

class TecdocModel(models.Model):
 
    objects = TecdocManager()

    class Meta:
        abstract = True
        managed = False


class Description(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TEX_ID')
    text = models.TextField(u'Текст', db_column='TEX_TEXT')

    objects = TecdocManager()

    class Meta:
         db_table = 'DES_TEXTS'


class Language(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LNG_ID')

    designation = models.ForeignKey('tecdoc.Designation',
                                    verbose_name=u'Обозначение',
                                    db_column='LNG_DES_ID',
                                    blank=True, null=True) 

    iso_code = models.CharField(u'Код ISO2', max_length=6,
                                db_column='LNG_ISO2',
                                blank=True, null=True)

    codepage = models.CharField(u'Кодировка', max_length=30,
                                db_column='LNG_CODEPAGE',
                                blank=True, null=True)

    objects = TecdocManager()

    class Meta:
         db_table = 'LANGUAGES'


class DesignationBase(TecdocModel):
    class Meta:
        abstract = True

    def __unicode__(self):
        return self.description.text


class Designation(DesignationBase):

    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DES_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             related_name='lang_designation',
                             db_column='DES_LNG_ID')

    description = models.ForeignKey(Description,
                                    verbose_name=u'Описание',
                                    db_column='DES_TEX_ID')

    objects = TecdocManager()

    class Meta:
         db_table = 'DESIGNATIONS'


class CountryDesignation(DesignationBase):

    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='CDS_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             db_column='CDS_LNG_ID')

    description = models.ForeignKey(Description,
                                    verbose_name=u'Описание',
                                    db_column='CDS_TEX_ID')

    objects = TecdocManager()

    class Meta:
         db_table = 'COUNTRY_DESIGNATIONS'


class Country(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='COU_ID')

    iso_code = models.CharField(u'Код ISO2', max_length=6,
                                db_column='COU_ISO2',
                                blank=True, null=True)

    designation = models.ForeignKey(CountryDesignation,
                                    verbose_name=u'Обозначение',
                                    db_column='COU_DES_ID')

    currency_code = models.CharField(u'Код Валюты', max_length=9,
                                     db_column='COU_CURRENCY_CODE',
                                     blank=True, null=True)

    objects = TecdocManager()

    class Meta:
         db_table = 'COUNTRIES'


class Brand(TecdocModel):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='BRA_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='BRA_BRAND',
                             blank=True, null=True)

    code = models.CharField(u'Название', max_length=30,
                             db_column='BRA_MFC_CODE',
                             blank=True, null=True)

    objects = TecdocManager()

    class Meta:
         db_table = 'BRANDS'
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

    objects = TecdocManager()

    class Meta:
         db_table = 'MANUFACTURERS'
         ordering = ['title']

    def __unicode__(self):
        return self.title


class Supplier(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='SUP_ID')

    title = models.CharField(u'Название', max_length=60,
                             db_column='SUP_BRAND',
                             blank=True, null=True)

    objects = TecdocManager()

    class Meta:
         db_table = 'SUPPLIERS'


class CarModelManager(TecdocManager):
    def get_models(self, brand, date_min, date_max,
                  search_text=None, lang=tdsettings.LANG_ID):

        query = self.get_models_wp(brand, lang=lang)

        if date_min:
             # TODO
             pass

        if search_text:
             query.filter(designation__description__text__icontains=search_text)

        return query

    def get_models_wp(self, brand, lang=tdsettings.LANG_ID):
        query = self.get_query_set()
        query = query.select_related('manufacturer',
                                     'designation__description')
        query = query.filter(manufacturer=brand,
                             designation__lang=lang)

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
        return u'(%s)%s' % (self.id, self.manufacturer)


    def __unicode2__(self):
        return u'(%s)%s - %s' % (self.id, self.manufacturer,
                                 u', '.join(unicode(x) for x in self.get_cd()))

    def get_cd(self):
        return CountryDesignation.objects.filter(id=self.designation_id,
                                                 lang=tdsettings.LANG_ID)

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

    objects = TecdocManager()

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

    objects = TecdocManager()

    class Meta:
         db_table = 'TYPES'
         ordering = ['sorting', 'production_start']

    #def __unicode__(self):
    #    return u'(%s) %s' % (self.id,
    #                         self.designation)

    def __unicode__(self):
        return u'(%s)%s - %s' % (self.id, self.model,
                                 u', '.join(unicode(x) for x in self.get_cd()))

    def get_cd(self):
        return CountryDesignation.objects.filter(id=self.designation_id,
                                                 lang=tdsettings.LANG_ID)



class CarTypeEngine(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LTE_TYP_ID')

    car_type = models.ForeignKey(CarType,
                                 verbose_name=u'Тип',
                                 db_column='LTE_NR')

    engine = models.ForeignKey(Engine,
                               verbose_name=u'Двигатель',
                               db_column='LTE_ENG_iD')

    production_start = models.IntegerField(u'Начало производства',
                                        db_column='LTE_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='LTE_PCON_END')

    objects = TecdocManager()

    class Meta:
         db_table = 'LINK_TYP_ENG'


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

    designation = models.ForeignKey(Designation,
                                    verbose_name=u'Обозначение',
                                    db_column='STR_DES_ID')

    def __unicode__(self):
        return u'(%s)%s' % (self.id,
                            u', '.join(unicode(x) for x in self.get_cd()))

    def get_cd(self):
        return Designation.objects.filter(id=self.designation_id,
                                          lang=tdsettings.LANG_ID)

    objects = TecdocManager()

    class Meta:
         db_table = 'SEARCH_TREE'


class Part(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ART_ID')

    images = models.ManyToManyField('tecdoc.Image', verbose_name=u'Изображения',
                                    through='tecdoc.PartImage')

    objects = TecdocManager()

    class Meta:
         db_table = 'ARTICLES'


class GenericPart(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GA_ID')

    objects = TecdocManager()

    class Meta:
         db_table = 'GENERIC_ARTICLES'


class PartGroup(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LA_ID')

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LA_ART_ID')

    global_part = models.ForeignKey(GenericPart,
                                    verbose_name=u'Оригинальная? Запчать',
                                    db_column='LA_GA_ID')
    
    objects = TecdocManager()

    class Meta:
         db_table = 'LINK_ART'


class PartGenericPart(TecdocModel):

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LAG_ART_ID')

    generic_part = models.ForeignKey(GenericPart, verbose_name=u'Запчасть',
                                    db_column='LAG_GA_ID')

    supplier = models.ForeignKey(Supplier, verbose_name=u'Поставщик',
                                 db_column='LAG_SUP_ID')

    class Meta:
         db_table = 'LINK_ART_GA'


class Property(TecdocModel):
    objects = TecdocManager()

    class Meta:
         db_table = 'ARTICLE_CRITERIA'


class FileType(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DOC_TYPE')

    ext = models.CharField(max_length=9, db_column='DOC_EXTENSION')

    objects = TecdocManager()

    class Meta:
         db_table = 'DOC_TYPES'



class Image(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GRA_ID')

    type = models.ForeignKey(FileType, verbose_name=u'Тип',
                             db_column='GRA_DOC_TYPE')

    objects = TecdocManager()

    class Meta:
         db_table = 'GRAPHICS'


class PartImage(TecdocModel):

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    image = models.ForeignKey(Image, verbose_name=u'Изображение',
                              db_column='LGA_GRA_ID')

    objects = TecdocManager()

    class Meta:
         db_table = 'LINK_GRA_ART'


class PdfFile(Image):

    class Meta:
        proxy = True


#function LookupByNumber
#function LookupAnalog
#function GetPartInfo
#function GetPropertys
