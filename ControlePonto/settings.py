# -*- coding: UTF-8 -*-
# Django settings for ControlePonto project.
import os
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
    ('Fernando Freitas Alves', 'ffreitasalves@gmail.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'      # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(SITE_ROOT, 'relogioponto.db') # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pt-BR'

#PRA USAR TUDO LOCALMENTE:
#USE_L10N = True
DATE_INPUT_FORMATS = ('%d/%m/%Y',)
SHORT_DATE_FORMAT = 'd/m/Y'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media2/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media2/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media2/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '!8b=fz7gia#49e)!5+6_aax(f-vc(7*xevzr+i3d*c(6zi@o%o'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'ControlePonto.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'Templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'Controle',
)

LOGIN_URL = '/entrar/'
LOGIN_REDIRECT_URL = '/relatorios/'
LOGOUT_URL = '/entrar/'

### Settings do Active Directory

AD_DNS_NAME = '' #IP DO DNS
AD_LDAP_PORT = 389

SEARCH_LEVEL = "ONELEVEL" #OPÇÕES: BASE, ONELEVEL ou SUBTREE

#Coloque as DN`s dos grupos que terão acesso ao sistema, exemplo: 'ou=Estagiarios,dc=xpto,dc=empresa,dc=br',
AD_SEARCH_DN = (
    'ou=MonitoresSTI,dc=sti,dc=fea,dc=br',
    'OU=FUNCIONARIOS_STI,DC=STI,DC=FEA,DC=BR',
)

#Coloque as DN`s dos grupos que terão acesso administrativo
AD_ADMGROUP_DN = (
    'cn=ManualADM,cn=users,dc=sti,dc=fea,dc=br',
    'cn=FuncionarioSTI,cn=users,dc=sti,dc=fea,dc=br',
)

#Coloque as DN`s dos grupos que terão acesso ao sistema, exemplo: 'ou=Estagiarios,dc=xpto,dc=empresa,dc=br',
AD_GROUP_DN = (
    'cn=MonitoresSTI,cn=users,dc=sti,dc=fea,dc=br',

)

#Qualificação do domínio:
AD_NT4_DOMAIN = '' #ex: xpto.empresa.br

AD_SEARCH_FIELDS = ['sAMAccountName','memberOf']

AD_LDAP_URL = 'ldap://' #Coloque o IP do servidor ldap

AUTHENTICATION_BACKENDS = (
    'auth.ActiveDirectoryBackend',
    'django.contrib.auth.backends.ModelBackend',
)
