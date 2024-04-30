"""
WSGI config for webapps2024 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import threading
from django.core.wsgi import get_wsgi_application
from rpc_server import thrift_server

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2024.settings')

threading.Thread(target=thrift_server).start()

application = get_wsgi_application()
