"""
============================================================
MODELS - Modelos do banco de dados
============================================================
Cada classe aqui representa uma TABELA no banco de dados PostgreSQL.
O Django ORM (Object-Relational Mapping) converte esses modelos Python
em tabelas SQL automaticamente.

Para aplicar no banco: python manage.py makemigrations && python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# ============================================================
# FORNECEDOR
# ============================================================
class Fornecedor(models.Model):
    """
    Representa uma empresa ou pessoa que fornece itens ao patrimônio.
    Um fornecedor pode estar associado a vários itens patrimoniais.
    """
    nome         = models.CharField(max_length=255, verbose_name='Nome')
    cnpj         = models.CharField(max_length=20, blank=True, verbose_name='CNPJ')
    contato      = models.CharField(max_length=255, blank=True, verbose_name='Pessoa de Contato')
    email        = models.EmailField(blank=True, verbose_name='E-mail')
    telefone     = models.CharField(max_length=20, blank=True, verbose_name='Telefone')
    endereco     = models.TextField(blank=True, verbose_name='Endereço')
    criado_em    = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']  # Ordena alfabeticamente por padrão

    def __str__(self):
        # Retorna o nome do fornecedor quando exibido como texto
        return self.nome


# ============================================================
# LOCALIZAÇÃO
# ============================================================
class Localizacao(models.Model):
    """
    Representa um local físico onde os itens patrimoniais estão guardados.
    Exemplo: 'Sala 101', 'Almoxarifado', 'Diretoria'.
    """
    nome              = models.CharField(max_length=255, verbose_name='Nome do Local')
    # Responsável pelo local - se o usuário for deletado, o campo vira NULL
    responsavel       = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Responsável'
    )
    # Guarda o nome do responsável como texto (caso o usuário seja deletado)
    responsavel_nome  = models.CharField(max_length=255, blank=True, verbose_name='Nome do Responsável')
    criado_em         = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Localização'
        verbose_name_plural = 'Localizações'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# ============================================================
# ITEM PATRIMONIAL
# ============================================================
class PatrimonioItem(models.Model):
    """
    Representa um bem patrimonial da organização.
    É o modelo principal do sistema - ex: computador, mesa, veículo.

    Campos obrigatórios: numero_chapa, nome, categoria, status
    Campos opcionais: todos os outros
    """

    # --- Opções de Status ---
    STATUS_ATIVO       = 'ativo'
    STATUS_MANUTENCAO  = 'manutencao'
    STATUS_BAIXADO     = 'baixado'
    STATUS_CHOICES = [
        (STATUS_ATIVO,      'Ativo'),
        (STATUS_MANUTENCAO, 'Manutenção'),
        (STATUS_BAIXADO,    'Baixado'),
    ]

    # --- Campos principais ---
    numero_chapa    = models.IntegerField(
        unique=True,
        verbose_name='Número da Chapa',
        help_text='Identificador único do item (ex: 1001)'
    )
    nome            = models.CharField(max_length=255, verbose_name='Nome do Item')
    categoria       = models.CharField(max_length=100, blank=True, verbose_name='Categoria')
    status          = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ATIVO,
        verbose_name='Status'
    )

    # --- Localização ---
    # ForeignKey = relação muitos-para-um (vários itens podem estar no mesmo local)
    localizacao     = models.ForeignKey(
        Localizacao,
        on_delete=models.SET_NULL,  # Se o local for deletado, o campo vira NULL
        null=True,
        blank=True,
        verbose_name='Localização'
    )
    responsavel     = models.CharField(max_length=255, blank=True, verbose_name='Responsável')

    # --- Dados de aquisição ---
    data_aquisicao  = models.DateField(null=True, blank=True, verbose_name='Data de Aquisição')
    valor           = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Valor (R$)',
        validators=[MinValueValidator(0)]  # Valor não pode ser negativo
    )

    # --- Fornecedor ---
    fornecedor      = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Fornecedor'
    )

    # --- Descrição ---
    descricao       = models.TextField(blank=True, verbose_name='Descrição / Observações')

    # --- Rastreabilidade ---
    criado_por      = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='itens_criados',
        verbose_name='Criado por'
    )
    criado_por_nome = models.CharField(max_length=255, blank=True, verbose_name='Nome de quem cadastrou')

    # --- Controle automático de datas ---
    criado_em       = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em   = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Item Patrimonial'
        verbose_name_plural = 'Itens Patrimoniais'
        ordering = ['numero_chapa']  # Ordena pelo número da chapa por padrão

    def __str__(self):
        return f'[{self.numero_chapa}] {self.nome}'

    @classmethod
    def proximo_numero_chapa(cls):
        """
        Retorna o próximo número de chapa disponível.
        Começa em 1001 e incrementa automaticamente.
        """
        ultimo = cls.objects.order_by('-numero_chapa').first()
        if ultimo:
            return ultimo.numero_chapa + 1
        return 1001  # Número inicial padrão

    def get_status_badge_class(self):
        """Retorna a classe CSS do badge de acordo com o status."""
        classes = {
            self.STATUS_ATIVO:      'badge-ativo',
            self.STATUS_MANUTENCAO: 'badge-manutencao',
            self.STATUS_BAIXADO:    'badge-baixado',
        }
        return classes.get(self.status, 'badge-ativo')


# ============================================================
# LOG DE AUDITORIA
# ============================================================
class LogAuditoria(models.Model):
    """
    Registra TODAS as ações realizadas no sistema.
    Permite rastrear quem fez o quê e quando.

    Exemplos de log:
    - "Admin criou o item [1005] Notebook Dell"
    - "João importou 25 itens do arquivo inventario.xlsx"
    - "Maria fez login no sistema"
    """

    # --- Tipos de ação ---
    ACAO_CRIAR    = 'CRIAR'
    ACAO_EDITAR   = 'EDITAR'
    ACAO_DELETAR  = 'DELETAR'
    ACAO_LOGIN    = 'LOGIN'
    ACAO_LOGOUT   = 'LOGOUT'
    ACAO_IMPORTAR = 'IMPORTAR'
    ACAO_CHOICES = [
        (ACAO_CRIAR,    'Criar'),
        (ACAO_EDITAR,   'Editar'),
        (ACAO_DELETAR,  'Deletar'),
        (ACAO_LOGIN,    'Login'),
        (ACAO_LOGOUT,   'Logout'),
        (ACAO_IMPORTAR, 'Importar'),
    ]

    # --- Tipos de entidade ---
    ENTIDADE_PATRIMONIO  = 'PATRIMONIO'
    ENTIDADE_FORNECEDOR  = 'FORNECEDOR'
    ENTIDADE_LOCALIZACAO = 'LOCALIZACAO'
    ENTIDADE_USUARIO     = 'USUARIO'
    ENTIDADE_SISTEMA     = 'SISTEMA'
    ENTIDADE_CHOICES = [
        (ENTIDADE_PATRIMONIO,  'Patrimônio'),
        (ENTIDADE_FORNECEDOR,  'Fornecedor'),
        (ENTIDADE_LOCALIZACAO, 'Localização'),
        (ENTIDADE_USUARIO,     'Usuário'),
        (ENTIDADE_SISTEMA,     'Sistema'),
    ]

    # --- Campos do log ---
    acao           = models.CharField(max_length=20, choices=ACAO_CHOICES, verbose_name='Ação')
    tipo_entidade  = models.CharField(max_length=20, choices=ENTIDADE_CHOICES, verbose_name='Tipo')
    descricao      = models.TextField(verbose_name='Descrição')

    # Usuário que realizou a ação (SET_NULL para não perder o log se o usuário for deletado)
    usuario        = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário'
    )
    usuario_nome   = models.CharField(max_length=255, verbose_name='Nome do Usuário')

    # Referência ao item afetado (guardado como texto para não depender do objeto existir)
    entidade_id    = models.CharField(max_length=50, blank=True, verbose_name='ID da Entidade')
    entidade_nome  = models.CharField(max_length=255, blank=True, verbose_name='Nome da Entidade')

    criado_em      = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')

    class Meta:
        verbose_name = 'Log de Auditoria'
        verbose_name_plural = 'Logs de Auditoria'
        ordering = ['-criado_em']  # Mais recentes primeiro

    def __str__(self):
        return f'[{self.criado_em:%d/%m/%Y %H:%M}] {self.usuario_nome} - {self.acao} {self.tipo_entidade}'

    @classmethod
    def registrar(cls, acao, tipo_entidade, descricao, usuario=None,
                  entidade_id='', entidade_nome=''):
        """
        Método auxiliar para criar um log de forma simples.

        Uso: LogAuditoria.registrar(
            acao=LogAuditoria.ACAO_CRIAR,
            tipo_entidade=LogAuditoria.ENTIDADE_PATRIMONIO,
            descricao='Criou o item Notebook Dell',
            usuario=request.user,
            entidade_id='1001',
            entidade_nome='Notebook Dell'
        )
        """
        usuario_nome = ''
        if usuario and usuario.is_authenticated:
            usuario_nome = usuario.get_full_name() or usuario.username

        cls.objects.create(
            acao=acao,
            tipo_entidade=tipo_entidade,
            descricao=descricao,
            usuario=usuario if (usuario and usuario.is_authenticated) else None,
            usuario_nome=usuario_nome,
            entidade_id=str(entidade_id),
            entidade_nome=entidade_nome,
        )


# ============================================================
# XLS DE REFERÊNCIA — dados persistidos no banco
# ============================================================
class XLSReferenciaItem(models.Model):
    """
    Guarda os dados extraídos do XLS de referência para auto-preenchimento.
    Substitui o arquivo xls_referencia.json (que era apagado no redeploy).
    """
    numero_chapa    = models.IntegerField(unique=True, verbose_name='Número da Chapa')
    nome            = models.CharField(max_length=500, blank=True, verbose_name='Nome/Descrição')
    data_aquisicao  = models.CharField(max_length=10, blank=True, verbose_name='Data (ISO)')
    local           = models.CharField(max_length=255, blank=True, verbose_name='Local 2')
    status          = models.CharField(max_length=20, blank=True, verbose_name='Status')

    class Meta:
        verbose_name = 'Item XLS Referência'
        verbose_name_plural = 'Itens XLS Referência'

    def __str__(self):
        return f'[{self.numero_chapa}] {self.nome}'

