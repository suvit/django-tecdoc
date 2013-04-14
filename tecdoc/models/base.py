# -*- coding: utf-8 -

from django.db import models
from django.db.models.base import ModelBase

from tecdoc.conf import TecdocConf as tdsettings


class TecdocManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManager, self).get_query_set(*args, **kwargs)
                                          .using(tdsettings.DATABASE)
                                               )

# XXX bug in django - managed attr don`t inherited
class TecdocModelBase(ModelBase):
    def __new__(cls, name, bases, attrs):
        new_class = super(TecdocModelBase, cls).__new__(cls, name, bases, attrs)
        new_class._meta.managed = False
        return new_class

class TecdocModel(models.Model):

    __metaclass__ = TecdocModelBase

    objects = TecdocManager()

    class Meta:
        abstract = True
        managed = False
        app_label = 'tecdoc'


class Description(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TEX_ID')
    text = models.TextField(u'Текст', db_column='TEX_TEXT')

    class Meta:
        db_table = 'DES_TEXTS'
        verbose_name = ''


class Text(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TMT_ID')

    text = models.TextField(u'Текст', db_column='TMT_TEXT')

    class Meta:
        db_table = 'TEXT_MODULE_TEXT'


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


class TextLanguage(DesignationBase):
    # XXX not a key
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='TMO_ID')

    lang = models.ForeignKey(Language,
                             verbose_name=u'Язык',
                             related_name='lang_designation',
                             db_column='TMO_LNG_ID')

    description = models.ForeignKey(Text,
                                    verbose_name=u'Описание',
                                    db_column='TMO_TMT_ID')

    class Meta:
        db_table = 'TEXT_MODULES'


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

    class Meta:
        db_table = 'COUNTRY_DESIGNATIONS'
