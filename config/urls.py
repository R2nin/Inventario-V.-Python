"""
============================================================
ARQUIVO DE URLs PRINCIPAL DO PROJETO
============================================================
Este arquivo é o "mapa de rotas" do site inteiro.
Cada URL que o usuário digitar no navegador é tratada aqui.

Formato: path('url/', view_function, name='nome_da_rota')
  - 'url/'         → o endereço que aparece no navegador
  - view_function  → a função Python que responde a essa URL
  - name=          → apelido da URL (usado nos templates com {% url 'nome' %})
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Painel administrativo do Django (opcional, mas útil)
    # Acesse em: http://localhost:8000/admin/
    path('admin/', admin.site.urls),

    # Todas as URLs do nosso app "patrimonio" ficam no arquivo apps/patrimonio/urls.py
    # O prefixo '' significa que começam na raiz do site (ex: /login/, /dashboard/)
    path('', include('apps.patrimonio.urls')),
]

# Em desenvolvimento, serve os arquivos de mídia (uploads) localmente
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
