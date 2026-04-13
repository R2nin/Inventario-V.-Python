"""
Configuração do App Django "patrimonio".
O Django precisa deste arquivo para reconhecer o app.
"""
from django.apps import AppConfig


class PatrimonioConfig(AppConfig):
    # Tipo de campo padrão para chaves primárias
    default_auto_field = 'django.db.models.BigAutoField'
    # Caminho completo do app (deve corresponder ao INSTALLED_APPS em settings.py)
    name = 'apps.patrimonio'
    # Nome legível exibido no admin do Django
    verbose_name = 'Gestão Patrimonial'
