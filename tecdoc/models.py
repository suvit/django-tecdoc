# -*- coding: utf-8 -

from django.db import models

from tecdoc.conf import TecdocConf as tdsettings


class TecdocManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManager, self).get_query_set(*args, **kwargs)
                                          .using('tecdoc')
                                          )


class Description(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TEX_ID')
    text = models.TextField(u'Текст', db_column='TEX_TEXT')

    objects = TecdocManager()


class Language(models.Manager):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='LNG_ID')

    iso_code = models.CharField(u'Код ISO2', max_length=6,
                                db_column='LNG_ISO2',
                                blank=True, null=True)

    codepage = models.CharField(u'Кодировка', max_length=30,
                                db_column='LNG_CODEPAGE',
                                blank=True, null=True)

    objects = TecdocManager()


class Country(models.Model):
    objects = TecdocManager()


class CountryDesignation(models.Model):
    objects = TecdocManager()

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='CDS_ID')

    lang = models.ForeighKey(Language,
                             verbose_name=u'Язык',
                             db_column='CDS_LNG_ID')

    description = models.ForeighKey(DESCRIPTION,
                                    verbose_name=u'Описание',
                                    db_column='CDS_TEX_ID')


class Manufacturer(models.Model):

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


class CarModelManager(TecdocManager);
    def get_models(self, brand, date_min, date_max,
                  search_text=None, lang=tdsettings.LANG_ID):
        query = self.get_query_set()
        query = query.select_related('manufacturer', 'country_designation')
        query = query.filter(manufacturer=brand,
                             country_designation__language=lang)

        if date_min:
             # TODO
             pass

        if search_text:
             query.filter(country_designation__description__text__icontains=search_text)

        return query

class CarModel(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MOD_ID')
    production_start = models.IntegerField(u'Начало производства',
                                        db_column='MOD_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='MOD_PCON_END')

    manufacturer = models.ForeighKey(Manufacturer,
                                     verbose_name=u'Производитель',
                                     db_column='MOD_MFA_ID')

    country_designation = models.ForeighKey(CountryDesignation,
                                     verbose_name=u'Обозначение',
                                     db_column='MOD_CDS_ID')

    objects = CarModelManager()

    class Meta:
         db_table = 'MODELS'

class CarType(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TYP_ID')

    objects = TecdocManager()

    class Meta:
         db_table = 'TYPES'

class CarSection(models.Model):
    # TODO use mptt here
    objects = TecdocManager()

    class Meta:
         db_table = 'SEARCH_TREE'


class Part(models.Model):
    objects = TecdocManager()

class Property(models.Model):
    objects = TecdocManager()

class Image(models.Model):
    objects = TecdocManager()

class PdfFile(models.Model):
    objects = TecdocManager()
