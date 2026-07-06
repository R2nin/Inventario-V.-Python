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
    path('usuarios/',                      views.usuario_lista,       name='usuario_lista'),
    path('usuarios/novo/',                 views.usuario_criar,        name='usuario_criar'),
    path('usuarios/<int:pk>/deletar/',     views.usuario_deletar,      name='usuario_deletar'),
    path('usuarios/<int:pk>/setores/',     views.usuario_permissoes,   name='usuario_permissoes'),

    # ----------------------------------------------------------
    # LOGS DE AUDITORIA
    # ----------------------------------------------------------
    path('logs/', views.log_lista, name='log_lista'),

    # ----------------------------------------------------------
    # QR CODE
    # ----------------------------------------------------------
    # Leitor de QR Code via câmera (inventário por localização)
    path('scanner/',                              views.scanner_qrcode,        name='scanner_qrcode'),
    # API JSON: dados de um item por chapa (usado pelo scanner)
    path('scanner/api/item/<int:chapa>/',         views.api_item_por_chapa,    name='api_item_por_chapa'),
    # API JSON: salva localização de um item (usado pelo scanner)
    path('scanner/api/item/<int:pk>/salvar/',     views.api_salvar_localizacao, name='api_salvar_localizacao'),
    # Leitor QR para conferência avulsa com exportação XLS
    path('leitor-qr/',                            views.leitor_qr_conferencia, name='leitor_qr_conferencia'),
    path('leitor-qr/comparar/',                   views.comparar_leitor_xls,   name='comparar_leitor_xls'),
    # Busca item pelo número de chapa (chamado após leitura do QR)
    path('patrimonio/chapa/<int:numero_chapa>/',  views.buscar_por_chapa, name='buscar_por_chapa'),
    # Retorna a imagem PNG do QR Code de um item
    path('patrimonio/<int:pk>/qrcode.png',        views.gerar_qrcode,     name='gerar_qrcode'),
    # Página para visualizar e imprimir o QR Code
    path('patrimonio/<int:pk>/qrcode/',           views.pagina_qrcode,    name='pagina_qrcode'),
    # Página standalone para impressão da etiqueta térmica (sem base.html)
    path('patrimonio/<int:pk>/etiqueta/print/',   views.etiqueta_print,   name='etiqueta_print'),

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
    path('conferencia/',                                views.conferencia_inicio,               name='conferencia_inicio'),
    path('conferencia/importar-localizacoes/',          views.conferencia_importar_localizacoes, name='conferencia_importar_localizacoes'),
    path('conferencia/sala/',                           views.conferencia_sala,                 name='conferencia_sala'),
    path('conferencia/transferir/<int:pk>/',            views.conferencia_transferir,            name='conferencia_transferir'),
    path('conferencia/transferir-lote/',                views.conferencia_transferir_lote,       name='conferencia_transferir_lote'),
    path('conferencia/cadastrar-item/',                  views.conferencia_cadastrar_item,        name='conferencia_cadastrar_item'),
    path('conferencia/confirmar-xls/<int:pk>/',         views.conferencia_confirmar_xls,         name='conferencia_confirmar_xls'),
    path('conferencia/confirmar-xls-lote/',             views.conferencia_confirmar_xls_lote,    name='conferencia_confirmar_xls_lote'),
    path('conferencia/reset/',                            views.conferencia_reset,                name='conferencia_reset'),
    path('conferencia/remover-xls/',                      views.conferencia_remover_xls,           name='conferencia_remover_xls'),
    path('conferencia/enviar-para-fora/<int:pk>/',        views.conferencia_enviar_para_fora,     name='conferencia_enviar_para_fora'),
    path('conferencia/exportar/',                       views.conferencia_exportar,             name='conferencia_exportar'),
    path('conferencia/exportar-qrcodes/',               views.conferencia_exportar_qrcodes,     name='conferencia_exportar_qrcodes'),
    path('conferencia/comparar/',                       views.comparar_xls,                     name='comparar_xls'),

    # ----------------------------------------------------------
    # ETIQUETAS COLORIDAS
    # ----------------------------------------------------------
    path('etiquetas/', views.etiquetas_view, name='etiquetas'),

    # ----------------------------------------------------------
    # MANUTENÇÃO
    # ----------------------------------------------------------
    path('manutencao/',                        views.manutencao_lista,     name='manutencao_lista'),
    path('manutencao/registrar/',              views.manutencao_registrar, name='manutencao_registrar'),
    path('manutencao/<int:pk>/concluir/',      views.manutencao_concluir,  name='manutencao_concluir'),
    path('manutencao/<int:pk>/apagar/',        views.manutencao_apagar,    name='manutencao_apagar'),
]
