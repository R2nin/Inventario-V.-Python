"""
============================================================
ADMIN - Configuração do painel administrativo Django
============================================================
O Django tem um painel admin automático em /admin/ que
permite gerenciar todos os dados do banco de forma visual.

Para acessar: crie um superusuário com:
    python manage.py createsuperuser
"""

from django.contrib import admin
from .models import PatrimonioItem, Fornecedor, Localizacao, LogAuditoria


@admin.register(PatrimonioItem)
class PatrimonioItemAdmin(admin.ModelAdmin):
    list_display = ['numero_chapa', 'nome', 'categoria', 'localizacao', 'status', 'valor']
    list_filter  = ['status', 'categoria', 'localizacao']
    search_fields = ['nome', 'numero_chapa', 'responsavel']
    ordering = ['numero_chapa']


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'contato', 'email', 'telefone']
    search_fields = ['nome', 'cnpj']


@admin.register(Localizacao)
class LocalizacaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'responsavel_nome']
    search_fields = ['nome']


@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ['criado_em', 'usuario_nome', 'acao', 'tipo_entidade', 'descricao']
    list_filter  = ['acao', 'tipo_entidade']
    search_fields = ['usuario_nome', 'descricao']
    readonly_fields = ['criado_em']  # Log não pode ser editado
