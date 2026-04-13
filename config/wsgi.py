"""
============================================================
WSGI - Interface entre o servidor web e o Django
============================================================
WSGI (Web Server Gateway Interface) é o padrão Python para
comunicação entre servidores web (Gunicorn, Nginx) e aplicações.

Este arquivo é usado pelo Gunicorn em produção:
    gunicorn config.wsgi:application
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
