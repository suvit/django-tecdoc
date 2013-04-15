# -*- coding: utf-8 -
from django.db import models

from tecdoc.conf import TecdocConf as tdsettings
from tecdoc.models.base import (TecdocModel, TecdocManager,
                                TecdocManagerWithDes)


class FileType(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='DOC_TYPE')

    ext = models.CharField(max_length=9, db_column='DOC_EXTENSION')

    class Meta(TecdocModel.Meta):
        db_table = 'DOC_TYPES'


class File(TecdocModel):
    id = models.AutoField(u'Ид', primary_key=True,
                          db_column='GRA_ID')

    type = models.ForeignKey(FileType, verbose_name=u'Тип',
                             db_column='GRA_DOC_TYPE')

    db_number = models.IntegerField(u'Категория 1', db_column='GRA_TAB_NR')

    filename = models.IntegerField(u'Имя файла', db_column='GRA_GRD_ID')

    class Meta(TecdocModel.Meta):
        db_table = 'GRAPHICS'

    def absolute_path(self):
        return '%s%s' % (tdsettings.FILE_HOST, self.relative_path())


# TODO limit to img doc type
class Image(File):
    class Meta(File.Meta):
        proxy = True

    def relative_path(self):
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
        db_table = 'LINK_GRA_ART'


# TODO limit to pdf doc type
class PdfFile(File):
    class Meta(File.Meta):
        proxy = True

    def relative_path(self):
        return '/pdf/000%s.pdf' % (self.filename,)


class PartPdf(TecdocModel):

    part = models.ForeignKey('tecdoc.Part', verbose_name=u'Запчасть',
                             db_column='LGA_ART_ID')

    image = models.ForeignKey(PdfFile, verbose_name=u'Изображение',
                              db_column='LGA_GRA_ID')

    class Meta(TecdocModel.Meta):
        db_table = 'LINK_GRA_ART'
