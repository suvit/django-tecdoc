# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings


class TecdocManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManager, self).get_query_set(*args, **kwargs)
                                          .using(tdsettings.DATABASE)
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


class DesignationManager(TecdocManager):
    def get_query_set(self, *args, **kwargs):
        return (super(DesignationManager, self).get_query_set(*args, **kwargs)
                                               .filter(lang=tdsettings.LANG_ID)
                                               .select_related('description')
                                               )


class DesignationBase(TecdocModel):

    objects = DesignationManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.description.text


class TecdocManagerWithDes(TecdocManager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManagerWithDes, self).get_query_set(*args, **kwargs)
                                                 .filter(designation__lang=tdsettings.LANG_ID)
                                                 .select_related('designation__description')                                          )


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

    objects = DesignationManager()

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

    objects = DesignationManager()

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

    objects = TecdocManagerWithDes()

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

    def __unicode__(self):
        return self.title


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

    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_TYP_ENG'


class RootSection(object):
    id = None
    level = 0

    def __unicode__(self):
        return u'Корень'

    def get_parts(self):
        return Part.objects.all()

    def get_children(self):
        return CarSection.objects.filter(parent__isnull=True)

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

    designation = models.ForeignKey(Designation,
                                    verbose_name=u'Обозначение',
                                    db_column='STR_DES_ID')

    def __unicode__(self):
        return u'%s' % (self.designation)

    objects = TecdocManagerWithDes()

    class Meta:
        db_table = 'SEARCH_TREE'

    def get_children(self):
        return self.children.all()

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
        return (Part.objects.filter(generic_parts__sections=self)
                            .select_related('supplier',
                                            'designation__description')
                            .prefetch_related('images')
                                 )


class Part(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='ART_ID')

    title = models.CharField(u'Название', max_length=66,
                             db_column='ART_ARTICLE_NR')

    supplier = models.ForeignKey(Supplier, verbose_name=u'Поставщик',
                                 db_column='ART_SUP_ID')

    # don`t use
    #short_designation = models.ForeignKey(Designation,
    #                                      verbose_name=u'Краткое Обозначение',
    #                                      db_column='ART_DES_ID',
    #                                      related_name='parts_with_short_designation')

    designation = models.ForeignKey(Designation,
                                    verbose_name=u'Обозначение',
                                    db_column='ART_COMPLETE_DES_ID')
                                    
    car_types = models.ManyToManyField('tecdoc.CarType',
                                       verbose_name=u'Модификации авто',
                                       through='tecdoc.PartTypeGroup',
                                       related_name='parts')

    generic_parts = models.ManyToManyField('tecdoc.GenericPart',
                                           verbose_name=u'Оригинальная? запчасть',
                                           through='tecdoc.PartGroup',
                                           related_name='parts')

    images = models.ManyToManyField('tecdoc.Image',
                                    verbose_name=u'Изображения',
                                    through='tecdoc.PartImage',
                                    related_name='parts')

    pdfs = models.ManyToManyField('tecdoc.PdfFile',
                                  verbose_name=u'Инструкция',
                                  through='tecdoc.PartPdf',
                                  related_name='parts') 

    objects = TecdocManagerWithDes()

    class Meta:
        db_table = 'ARTICLES'

    def __unicode__(self):
        return u'%s %s %s' % (self.designation, self.supplier, self.title)


class GenericPart(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GA_ID')

    objects = TecdocManager()

    sections = models.ManyToManyField('tecdoc.CarSection',
                                      verbose_name=u'Категории',
                                      through='tecdoc.SectionGenericPart',
                                      related_name='generic_parts')

    class Meta:
        db_table = 'GENERIC_ARTICLES'


class SectionGenericPart(TecdocModel):
    car_section = models.ForeignKey(CarSection, verbose_name=u'Категория',
                                    db_column='LGS_STR_ID')

    generic_part = models.ForeignKey(GenericPart,
                                   verbose_name=u'Оригинальная? Запчать',
                                   db_column='LGS_GA_ID')

    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_GA_STR'


class PartGroup(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LA_ID')

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LA_ART_ID')

    generic_part = models.ForeignKey(GenericPart,
                                    verbose_name=u'Оригинальная? Запчать',
                                    db_column='LA_GA_ID')
    
    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_ART'


class PartTypeGroup(TecdocModel):
    car_type = models.ForeignKey(CarType, verbose_name=u'Модификация модели',
                                 db_column='LAT_TYP_ID')

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LAT_LA_ID')
     
    generic_part = models.ForeignKey(GenericPart, verbose_name=u'Запчасть',
                                    db_column='LAT_GA_ID')

    supplier = models.ForeignKey(Supplier, verbose_name=u'Поставщик',
                                 db_column='LAT_SUP_ID')

    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_LA_TYP'


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


class File(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GRA_ID')

    type = models.ForeignKey(FileType, verbose_name=u'Тип',
                             db_column='GRA_DOC_TYPE')

    section1 = models.IntegerField(u'Категория 1', db_column='GRA_TAB_NR')

    filename = models.IntegerField(u'Имя файла', db_column='GRA_GRD_ID')


    objects = TecdocManager()

    class Meta:
        db_table = 'GRAPHICS'

    def absolute_path(self):
        return '%s%s' % (tdsettings.FILE_HOST, self.relative_path())


class Image(File):
    class Meta:
        proxy = True

    def relative_path(self):
        ext = self.type.ext.lower()
        return 'images/%s/%s.%s' % (self.section1,
                                    self.filename,
                                    ext == 'jp2' and 'jpg' or ext)

class PartImage(TecdocModel):

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    image = models.ForeignKey(Image, verbose_name=u'Изображение',
                              db_column='LGA_GRA_ID')

    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_GRA_ART'


class PdfFile(File):

    class Meta:
        proxy = True

    def relative_path(self):
        return '/pdf/000%s.pdf' % (self.filename,)

class PartPdf(TecdocModel):

    part = models.ForeignKey(Part, verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    image = models.ForeignKey(PdfFile, verbose_name=u'Изображение',
                              db_column='LGA_GRA_ID')

    objects = TecdocManager()

    class Meta:
        db_table = 'LINK_GRA_ART'


#function LookupByNumber
#function LookupAnalog
#function GetPartInfo
#function GetPropertys
