# -*- coding: utf-8 -
from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)


PDF_TYPE = 2

class FileType(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DOC_TYPE')

    ext = models.CharField(max_length=9, db_column='DOC_EXTENSION')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'DOC_TYPES'


class File(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GRA_ID')

    type = models.ForeignKey(FileType, verbose_name=u'Тип',
                             db_column='GRA_DOC_TYPE')

    db_number = models.IntegerField(u'Номер диска', db_column='GRA_TAB_NR')

    filename = models.IntegerField(u'Имя файла', db_column='GRA_GRD_ID')

    lang = models.IntegerField(u'Язык', db_column='GRA_LNG_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'GRAPHICS'

    def absolute_url(self):
        return '%s%s' % (tdsettings.FILE_HOST, self.relative_url())
    url = absolute_url


class ImageManager(TecdocManager):
    def get_query_set(self, *args, **kwargs):
        return (super(ImageManager, self).get_query_set(*args, **kwargs)
                                         .filter(lang__in=(tdsettings.LANG_ID, 255))
                                         .exclude(type=PDF_TYPE)
                                               )


class Image(File):

    objects = ImageManager()

    class Meta(File.Meta):
        proxy = True

    def relative_url(self):
        ext = self.type.ext.lower()
        return 'images/%s/%s.%s' % (self.db_number,
                                    self.filename,
                                    ext == 'jp2' and 'jpg' or ext)


class PartImage(TecdocModel):

    part = models.ForeignKey('tecdoc.Part', verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    image = models.ForeignKey(Image, verbose_name=u'Изображение',
                              db_column='LGA_GRA_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_GRA_ART'


class PdfManager(TecdocManager):
    def get_query_set(self, *args, **kwargs):
        return (super(PdfManager, self).get_query_set(*args, **kwargs)
                                       .filter(lang__in=(tdsettings.LANG_ID, 255),
                                               type=PDF_TYPE)
               )


class PdfFile(File):

    objects = PdfManager()

    class Meta(File.Meta):
        proxy = True

    def relative_url(self):
        return '/pdf/%s%s.pdf' % (self.id, str(self.lang).zfill(3))


class PartPdf(TecdocModel):

    part = models.ForeignKey('tecdoc.Part', verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    pdf = models.ForeignKey(PdfFile, verbose_name=u'Документация',
                            db_column='LGA_GRA_ID')

    class Meta(TecdocModel.Meta):
        db_table = tdsettings.DB_PREFIX + 'LINK_GRA_ART'
