from .settings_boilerplate import *  # noqa

# pylint: skip-file

DEBUG = True

AUDIT_DISABLE = False

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_partitioned_audit",
    "app.apps.AppConfig",
]

# By default, let's import some db configuration, to make sure it will work
# when using this file directly

from .settings_postgres15 import *  # noqa
