#!/usr/bin/env python
"""
============================================================
MANAGE.PY - Utilitário de linha de comando do Django
============================================================
Este é o arquivo principal para gerenciar o projeto via terminal.

Comandos mais usados:
  python manage.py runserver          → Inicia servidor de desenvolvimento
  python manage.py makemigrations     → Cria arquivos de migração do banco
  python manage.py migrate            → Aplica migrações no banco de dados
  python manage.py createsuperuser    → Cria usuário administrador
  python manage.py collectstatic      → Coleta arquivos estáticos para produção
"""

import os
import sys


def main():
    """Ponto de entrada para os comandos de gerenciamento do Django."""
    # Define qual arquivo de configurações usar
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se ele está instalado "
            "e se o ambiente virtual está ativado."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
