# Sistema de Gestão Patrimonial - Django

Sistema web completo para gerenciamento de patrimônio, desenvolvido com **Python/Django** e banco de dados **Supabase (PostgreSQL)**.

---

## Funcionalidades

- Login com controle de acesso (Admin / Usuário)
- CRUD completo de Itens Patrimoniais
- Importação em massa via Excel (.xlsx) e CSV
- Gestão de Fornecedores e Localizações
- Gerenciamento de Usuários (apenas admin)
- Log de Auditoria de todas as ações
- Geração de Relatório em PDF
- Dashboard com estatísticas

---

## PASSO 1: Pré-requisitos

Você precisa ter instalado:
- **Python 3.10+** → https://www.python.org/downloads/
- **Git** → https://git-scm.com/ (para deploy)

---

## PASSO 2: Configurar o ambiente local

Abra o terminal (Prompt de Comando ou PowerShell) nesta pasta.

### 2.1 Criar o ambiente virtual Python

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

> O ambiente virtual isola as dependências do projeto.
> Você verá `(venv)` no início do terminal quando estiver ativo.

### 2.2 Instalar as dependências

```bash
pip install -r requirements.txt
```

### 2.3 Criar o arquivo .env

Copie o arquivo de exemplo e preencha com seus dados:

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

Abra o arquivo `.env` e preencha:
- `SECRET_KEY` → gere uma em: https://djecrety.ir/
- `DATABASE_URL` → sua URL do Supabase (veja abaixo)

---

## PASSO 3: Configurar o Supabase

### 3.1 Criar conta e projeto
1. Acesse https://supabase.com e crie uma conta (gratuita)
2. Clique em **"New project"**
3. Defina um nome e senha para o banco

### 3.2 Obter a URL de conexão
1. No painel do Supabase, vá em: **Settings → Database**
2. Role até **"Connection string"**
3. Clique em **"URI"** e copie a URL
4. Substitua `[YOUR-PASSWORD]` pela senha que você criou
5. Cole no arquivo `.env` no campo `DATABASE_URL`

Exemplo:
```
DATABASE_URL=postgresql://postgres:minha_senha@db.abc123.supabase.co:5432/postgres
```

---

## PASSO 4: Preparar o banco de dados

```bash
# Cria as tabelas no banco (execute sempre após alterar models.py)
python manage.py makemigrations
python manage.py migrate

# Cria o primeiro usuário administrador
python manage.py createsuperuser
```

Siga as instruções para criar o usuário admin (nome, email, senha).

---

## PASSO 5: Rodar o servidor local

```bash
python manage.py runserver
```

Acesse no navegador: **http://localhost:8000**

---

## DEPLOY NO RAILWAY (recomendado - gratuito)

Railway é uma plataforma de deploy simples e gratuita para projetos Python.

### Passo 1: Preparar o projeto

```bash
# Instale o Git se não tiver
# Inicie um repositório Git nesta pasta:
git init
git add .
git commit -m "Primeiro commit - Sistema Patrimonial"
```

### Passo 2: Criar conta no Railway
1. Acesse https://railway.app
2. Clique em **"Start a New Project"**
3. Faça login com GitHub

### Passo 3: Conectar o projeto
1. Clique em **"Deploy from GitHub repo"**
2. Autorize o Railway a acessar seu GitHub
3. Selecione ou crie um repositório com este projeto
   - Se ainda não tem no GitHub: crie em https://github.com/new
   - Faça o push: `git remote add origin URL_DO_SEU_REPO && git push -u origin main`
4. O Railway detectará automaticamente que é Python/Django

### Passo 4: Configurar variáveis de ambiente no Railway
No painel do Railway, vá em **Variables** e adicione:

```
SECRET_KEY       = (gere uma nova em https://djecrety.ir/)
DEBUG            = False
ALLOWED_HOSTS    = seu-app.railway.app
DATABASE_URL     = (cole a URL do Supabase aqui)
```

### Passo 5: Configurar o comando de build
No Railway, vá em **Settings → Deploy** e configure:

**Build Command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Passo 6: Deploy!
O Railway fará o deploy automaticamente. Após concluir:
1. Clique em **"Generate Domain"** para obter uma URL pública
2. Acesse a URL gerada
3. Crie seu superusuário via terminal do Railway:
   ```
   python manage.py createsuperuser
   ```

---

## DEPLOY NO RENDER (alternativa gratuita)

### Passo 1: Criar conta em https://render.com

### Passo 2: Novo Web Service
1. Clique em **"New → Web Service"**
2. Conecte seu repositório GitHub

### Passo 3: Configurações
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command:** `gunicorn config.wsgi:application`

### Passo 4: Environment Variables
Adicione as mesmas variáveis do passo Railway acima.

---

## Estrutura do Projeto

```
inventario_django/
├── manage.py              ← Comandos Django
├── requirements.txt       ← Dependências Python
├── .env.example           ← Modelo de configuração
├── Procfile               ← Comando de start (deploy)
├── LEIA-ME.md             ← Este arquivo
│
├── config/                ← Configurações do projeto
│   ├── settings.py        ← Configurações principais
│   ├── urls.py            ← URLs raiz
│   └── wsgi.py            ← Interface servidor web
│
└── apps/
    └── patrimonio/        ← App principal
        ├── models.py      ← Modelos do banco de dados
        ├── views.py       ← Lógica de cada página
        ├── urls.py        ← URLs do app
        ├── forms.py       ← Formulários
        ├── admin.py       ← Painel administrativo
        ├── utils.py       ← Utilitários (PDF, Excel)
        └── templates/     ← Arquivos HTML
```

---

## Comandos úteis

```bash
# Ativar ambiente virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar/aplicar migrações após alterar models.py
python manage.py makemigrations
python manage.py migrate

# Criar usuário administrador
python manage.py createsuperuser

# Coletar arquivos estáticos (necessário antes do deploy)
python manage.py collectstatic

# Ver todas as URLs disponíveis
python manage.py show_urls
```

---

## Perfis de usuário

| Perfil | Pode fazer |
|--------|-----------|
| **Admin** (`is_staff=True`) | Tudo: criar, editar, deletar, importar, gerenciar usuários |
| **Usuário** | Visualizar patrimônio, fornecedores, localizações e logs |

---

## Dúvidas frequentes

**Como resetar a senha de um usuário?**
```bash
python manage.py changepassword nome_do_usuario
```

**Como ver os logs de erro em produção?**
No Railway/Render, acesse a aba **"Logs"** do seu serviço.

**O CSS não aparece em produção (página sem estilo)?**
Execute `python manage.py collectstatic` e certifique-se de que `whitenoise` está no `MIDDLEWARE` do `settings.py`.
