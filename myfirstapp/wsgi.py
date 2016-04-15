"""
WSGI config for myfirstapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

## Tady není nic k vidění. Tento soubor byl vygenerovaný automaticky,
## a slouží k tomu, aby náš projekt mohl běžet na serverech které
## podporují standard WSGI.
## Neboli, prostě, aby to fungovalo :)

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myfirstapp.settings")

application = get_wsgi_application()
