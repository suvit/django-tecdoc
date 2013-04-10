# -*- coding: utf-8 -

from appconf import AppConf

DE_LANG = 1
EN_LANG = 3
RU_LANG = 16

class TecdocConf(AppConf):

    DATABASE = 'tecdoc'

    LANG_ID = RU_LANG
    APP_ROOT = '.'
