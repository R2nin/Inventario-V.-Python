"""
============================================================
CONFIGURAÇÕES PRINCIPAIS DO PROJETO DJANGO
============================================================
Este arquivo controla TUDO sobre como o Django funciona:
banco de dados, segurança, apps instalados, etc.

As informações sensíveis (senhas, chaves) ficam no arquivo .env
e são lidas aqui de forma segura pela biblioteca "decouple".
"""

import os
from pathlib import Path
from decouple import config, Csv
import dj_database_url  # Converte a URL do banco em configuração Django

# ------------------------------------------------------------
# CAMINHOS BASE
# ------------------------------------------------------------
# BASE_DIR aponta para a pasta raiz do projeto (onde fica manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------
# SEGURANÇA
# ------------------------------------------------------------
# Chave secreta do Django - lida do arquivo .env
# NUNCA coloque a chave real diretamente aqui!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-mude-esta-chave-no-arquivo-env')

# DEBUG=True mostra erros detalhados (use apenas em desenvolvimento!)
# Em produção, sempre False
DEBUG = config('DEBUG', default=True, cast=bool)

# Lista de domínios/IPs que podem acessar o site
# Em produção: ['meusite.railway.app', 'meudominio.com']
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# ------------------------------------------------------------
# APLICAÇÕES INSTALADAS
# ------------------------------------------------------------
# Lista de todos os "apps" que o Django deve carregar
INSTALLED_APPS = [
    # Apps padrão do Django
    'django.contrib.admin',          # Painel administrativo automático
    'django.contrib.auth',           # Sistema de autenticação (login/logout)
    'django.contrib.contenttypes',   # Sistema de tipos de conteúdo
    'django.contrib.sessions',       # Gerenciamento de sessões de usuário
    'django.contrib.messages',       # Sistema de mensagens flash (alertas)
    'django.contrib.staticfiles',    # Gerenciamento de arquivos estáticos (CSS, JS)

    # Nosso app principal
    'apps.patrimonio',
]

# ------------------------------------------------------------
# MIDDLEWARES
# ------------------------------------------------------------
# Middlewares são camadas que processam cada requisição/resposta
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # Proteção contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------
# URLS
# ------------------------------------------------------------
# Arquivo principal de URLs do projeto
ROOT_URLCONF = 'config.urls'

# ------------------------------------------------------------
# TEMPLATES (HTML)
# ------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Django vai procurar templates nas pastas "templates" de cada app
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necessário para login
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------
# SERVIDOR WSGI (para deploy)
# ------------------------------------------------------------
WSGI_APPLICATION = 'config.wsgi.application'

# ------------------------------------------------------------
# BANCO DE DADOS
# ------------------------------------------------------------
# Lê a URL de conexão do arquivo .env e converte para o formato Django
# Exemplo de DATABASE_URL: postgresql://user:senha@host:5432/banco
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600,  # Mantém conexões abertas por 10 minutos (performance)
    )
}

# ------------------------------------------------------------
# VALIDAÇÃO DE SENHAS
# ------------------------------------------------------------
# Regras para senhas dos usuários
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------
# INTERNACIONALIZAÇÃO
# ------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'      # Idioma: Português do Brasil
TIME_ZONE = 'America/Sao_Paulo'  # Fuso horário: Brasília
USE_I18N = True               # Ativa internacionalização
USE_TZ = True                 # Usa timezone-aware datetimes

# ------------------------------------------------------------
# ARQUIVOS ESTÁTICOS (CSS, JavaScript, Imagens)
# ------------------------------------------------------------
# URL base para acessar arquivos estáticos no navegador
STATIC_URL = '/static/'

# Pasta onde o Django coleta todos os arquivos estáticos para produção
# (gerada pelo comando: python manage.py collectstatic)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Pastas extras onde o Django procura arquivos estáticos
STATICFILES_DIRS = [BASE_DIR / 'static']

# WhiteNoise: comprime e serve arquivos estáticos de forma eficiente
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ------------------------------------------------------------
# ARQUIVOS DE MÍDIA (uploads de usuários)
# ------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------
# AUTENTICAÇÃO
# ------------------------------------------------------------
# Onde redirecionar quando o usuário tenta acessar uma página sem estar logado
LOGIN_URL = '/login/'
# Onde redirecionar após o login bem-sucedido
LOGIN_REDIRECT_URL = '/'
# Onde redirecionar após o logout
LOGOUT_REDIRECT_URL = '/login/'

# ------------------------------------------------------------
# CHAVE PRIMÁRIA PADRÃO
# ------------------------------------------------------------
# Tipo de campo usado como chave primária quando não especificado
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------
# SEGURANÇA ADICIONAL (ativa em produção)
# ------------------------------------------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # Railway termina o SSL no proxy — não redirecionar aqui para evitar loop infinito
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
