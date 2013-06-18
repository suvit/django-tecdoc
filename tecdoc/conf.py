# -*- coding: utf-8 -

from appconf import AppConf

DE_LANG = 1
EN_LANG = 3
RU_LANG = 16

class TecdocConf(AppConf):

    DATABASE = 'tecdoc'
    DB_PREFIX = ''

    LANG_ID = RU_LANG
    APP_ROOT = '.'

    # Host for generation absolute path for images and pdf
    FILE_HOST = 'http://server/'
