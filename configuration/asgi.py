"""
ASGI config for configuration project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f'configuration.settings.{os.getenv("DJANGO_ENV", "local")}'
)

application = get_asgi_application()
