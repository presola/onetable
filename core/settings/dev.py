from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
import dj_database_url

from .config import *
DATABASES = local_database
default_object = dj_database_url.config(conn_max_age=600, ssl_require=True)

if 'ENGINE' in default_object:
    DATABASES['default'] = default_object

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p6_izlna_zfupnk57int)z2cew$qs7=q(hkm)f^1xhc%5pyurr'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *
except ImportError:
    pass
