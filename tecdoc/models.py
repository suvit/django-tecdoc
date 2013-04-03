# -*- coding: utf-8 -

from django.db import models

class TecdocManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return (super(TecdocManager, self).get_query_set(*args, **kwargs)
                                          .using('tecdoc')
                                          )

class Manufacturer(models.Model):

    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MFA_ID')
    title = models.CharField(u'Название', max_length=60,
                             db_column='MFA_BRAND',
                             blank=True, null=True)

    objects = TecdocManager()

    class Meta:
         db_table = 'MANUFACTURERS'
         ordering = ['title']

    def __unicode__(self):
        return self.title

'''$SQL='SELECT MOD_ID, TEX_TEXT AS MOD_CDS_TEXT, MOD_PCON_START, MOD_PCON_END 
FROM MODELS 
        INNER JOIN COUNTRY_DESIGNATIONS ON CDS_ID = MOD_CDS_ID
        INNER JOIN DES_TEXTS ON TEX_ID = CDS_TEX_ID
WHERE MOD_MFA_ID = '.$MFA_ID.' AND MOD_ID = '.$MOD_ID.' AND CDS_LNG_ID = '.$LNG_ID;''
'''

class CarModel(models.Model):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='MOD_ID')
    production_start = models.IntegerField(u'Начало производства',
                                        db_column='MOD_PCON_START')
    production_end = models.IntegerField(u'Конец производства',
                                      db_column='MOD_PCON_END')

    objects = TecdocManager()

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
