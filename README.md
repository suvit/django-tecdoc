django-tecdoc
=============

django integration with tecdoc db in mysql form


Installation
============================

`pip install django-tecdoc`

or

`pip install -e https://github.com/suvit/django-tecdoc#egg=tecdoc-dev`


Add separate db for `tecdoc`

   DATABASES = {
      'default': {
          ...
      },
      'tecdoc': {
          'ENGINE': 'django.db.backends.mysql',
          'NAME': 'tecdoc',
          'HOST': '',
          'USER': 'user',
          'PASSWORD': 'pass',
      }
   }

