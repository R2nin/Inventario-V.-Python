"""
============================================================
URLs DO APP PATRIMÔNIO
============================================================
Mapeamento de todas as URLs do sistema.

Formato: path('url/', view, name='nome')
  - name= é o apelido usado nos templates: {% url 'nome' %}
  - <int:pk> é um parâmetro numérico capturado da URL
    Ex: /patrimonio/5/editar/ → pk=5

Grupos de URLs:
  - Autenticação: /login/, /logout/
  - Dashboard: /
  - Patrimônio: /patrimonio/...
  - Fornecedores: /fornecedores/...
  - Localizações: /localizacoes/...
  - Usuários: /usuarios/...
  - Logs: /logs/
"""

from django.urls import path
from . import views

urlpatterns = [

    # ----------------------------------------------------------
    # AUTENTICAÇÃO
    # ----------------------------------------------------------
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ----------------------------------------------------------
    # DASHBOARD (página inicial)
    # ----------------------------------------------------------
    path('', views.dashboard, name='dashboard'),

    # ----------------------------------------------------------
    # PATRIMÔNIO
    # ----------------------------------------------------------
    path('patrimonio/',                    views.patrimonio_lista,    name='patrimonio_lista'),
    path('patrimonio/novo/',               views.patrimonio_criar,    name='patrimonio_criar'),
    path('patrimonio/importar/',           views.patrimonio_importar, name='patrimonio_importar'),
    path('patrimonio/relatorio/pdf/',      views.patrimonio_pdf,      name='patrimonio_pdf'),
    path('patrimonio/exportar/csv/',       views.exportar_csv,        name='exportar_csv'),
    path('patrimonio/<int:pk>/',           views.patrimonio_detalhe,  name='patrimonio_detalhe'),
    path('patrimonio/<int:pk>/editar/',    views.patrimonio_editar,   name='patrimonio_editar'),
    path('patrimonio/<int:pk>/deletar/',   views.patrimonio_deletar,  name='patrimonio_deletar'),

    # ----------------------------------------------------------
    # FORNECEDORES
    # ----------------------------------------------------------
    path('fornecedores/',                  views.fornecedor_lista,   name='fornecedor_lista'),
    path('fornecedores/novo/',             views.fornecedor_criar,   name='fornecedor_criar'),
    path('fornecedores/<int:pk>/editar/',  views.fornecedor_editar,  name='fornecedor_editar'),
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_deletar, name='fornecedor_deletar'),

    # ----------------------------------------------------------
    # LOCALIZAÇÕES
    # ----------------------------------------------------------
    path('localizacoes/',                  views.localizacao_lista,   name='localizacao_lista'),
    path('localizacoes/novo/',             views.localizacao_criar,   name='localizacao_criar'),
    path('localizacoes/<int:pk>/editar/',  views.localizacao_editar,  name='localizacao_editar'),
    path('localizacoes/<int:pk>/deletar/', views.localizacao_deletar, name='localizacao_deletar'),

    # ----------------------------------------------------------
    # USUÁRIOS
    # ----------------------------------------------------------
    path('usuarios/',                  views.usuario_lista,   name='usuario_lista'),
    path('usuarios/novo/',             views.usuario_criar,   name='usuario_criar'),
    path('usuarios/<int:pk>/deletar/', views.usuario_deletar, name='usuario_deletar'),

    # ----------------------------------------------------------
    # LOGS DE AUDITORIA
    # ----------------------------------------------------------
    path('logs/', views.log_lista, name='log_lista'),

    # ----------------------------------------------------------
    # QR CODE
    # ----------------------------------------------------------
    # Leitor de QR Code via câmera
    path('scanner/',                              views.scanner_qrcode,   name='scanner_qrcode'),
    # Busca item pelo número de chapa (chamado após leitura do QR)
    path('patrimonio/chapa/<int:numero_chapa>/',  views.buscar_por_chapa, name='buscar_por_chapa'),
    # Retorna a imagem PNG do QR Code de um item
    path('patrimonio/<int:pk>/qrcode.png',        views.gerar_qrcode,     name='gerar_qrcode'),
    # Página para visualizar e imprimir o QR Code
    path('patrimonio/<int:pk>/qrcode/',           views.pagina_qrcode,    name='pagina_qrcode'),

    # ----------------------------------------------------------
    # XLS DE REFERÊNCIA — AUTO-PREENCHIMENTO
    # ----------------------------------------------------------
    # Upload do XLS de referência
    path('patrimonio/xls-referencia/',            views.carregar_xls_referencia, name='carregar_xls_referencia'),
    # API JSON: retorna dados de um item pelo número de chapa
    path('patrimonio/xls-ref/<int:chapa>/',       views.buscar_dados_xls,        name='buscar_dados_xls'),

    # ----------------------------------------------------------
    # MÓDULO DE CONFERÊNCIA DE INVENTÁRIO
    # ----------------------------------------------------------
    path('conferencia/',                          views.conferencia_inicio,               name='conferencia_inicio'),
    path('conferencia/importar-localizacoes/',    views.conferencia_importar_localizacoes, name='conferencia_importar_localizacoes'),
    path('conferencia/sala/',                     views.conferencia_sala,                 name='conferencia_sala'),
    path('conferencia/exportar/',                 views.conferencia_exportar,             name='conferencia_exportar'),
    path('conferencia/comparar/',                 views.comparar_xls,                     name='comparar_xls'),
]
