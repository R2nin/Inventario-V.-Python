"""
============================================================
FORMS - Formulários do sistema
============================================================
No Django, os "forms" fazem três coisas automaticamente:
  1. Geram o HTML dos campos do formulário
  2. Validam os dados enviados pelo usuário
  3. Salvam os dados no banco de dados (ModelForm)

Tipos usados aqui:
  - forms.ModelForm → gerado a partir de um Model (evita repetição de código)
  - forms.Form      → formulário manual (para casos especiais como login e importação)
"""

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import PatrimonioItem, Fornecedor, Localizacao


# ============================================================
# FORMULÁRIO DE LOGIN
# ============================================================
class LoginForm(forms.Form):
    """
    Formulário simples de login com usuário e senha.
    Não usa ModelForm porque não salva diretamente no banco.
    """
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Digite seu usuário',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Digite sua senha',
        })
    )


# ============================================================
# FORMULÁRIO DE ITEM PATRIMONIAL
# ============================================================
class PatrimonioItemForm(forms.ModelForm):
    """
    Formulário para criar e editar itens patrimoniais.
    ModelForm gera automaticamente os campos a partir do modelo.
    """

    class Meta:
        model = PatrimonioItem
        # Campos que aparecerão no formulário (na ordem desejada)
        fields = [
            'numero_chapa', 'nome',
            'localizacao', 'data_aquisicao', 'descricao',
        ]
        widgets = {
            'numero_chapa': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: 1001',
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Notebook Dell Inspiron',
            }),
            'localizacao': forms.Select(attrs={
                'class': 'form-input',
            }),
            'data_aquisicao': forms.DateInput(
                attrs={
                    'class': 'form-input',
                    'type': 'date',
                },
                format='%Y-%m-%d'
            ),
            'descricao': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Observações adicionais sobre o item...',
            }),
        }
        labels = {
            'numero_chapa': 'Número da Chapa',
            'nome': 'Nome do Item',
            'localizacao': 'Localização',
            'data_aquisicao': 'Data de Aquisição',
            'descricao': 'Descrição / Observações',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['localizacao'].empty_label = 'Selecione uma localização...'
        self.fields['data_aquisicao'].input_formats = ['%Y-%m-%d', '%d/%m/%Y']


# ============================================================
# FORMULÁRIO DE FORNECEDOR
# ============================================================
class FornecedorForm(forms.ModelForm):
    """
    Formulário para criar e editar fornecedores.
    """

    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'contato', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Razão social ou nome do fornecedor',
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '00.000.000/0001-00',
            }),
            'contato': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome da pessoa de contato',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@fornecedor.com.br',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '(11) 99999-9999',
            }),
            'endereco': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Endereço completo do fornecedor',
            }),
        }
        labels = {
            'nome': 'Nome / Razão Social',
            'cnpj': 'CNPJ',
            'contato': 'Pessoa de Contato',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'endereco': 'Endereço',
        }


# ============================================================
# FORMULÁRIO DE LOCALIZAÇÃO
# ============================================================
class LocalizacaoForm(forms.ModelForm):
    """
    Formulário para criar e editar localizações físicas.
    """

    class Meta:
        model = Localizacao
        fields = ['nome', 'responsavel', 'responsavel_nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Sala 101, Almoxarifado, Diretoria...',
            }),
            'responsavel': forms.Select(attrs={
                'class': 'form-input',
            }),
            'responsavel_nome': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do responsável pelo local',
            }),
        }
        labels = {
            'nome': 'Nome da Localização',
            'responsavel': 'Usuário Responsável',
            'responsavel_nome': 'Nome do Responsável',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['responsavel'].empty_label = 'Selecione um usuário (opcional)...'
        self.fields['responsavel'].required = False
        self.fields['responsavel_nome'].required = False


# ============================================================
# FORMULÁRIO DE CRIAÇÃO DE USUÁRIO
# ============================================================
class UsuarioForm(forms.ModelForm):
    """
    Formulário para o admin criar novos usuários do sistema.
    Inclui campo de senha com confirmação.
    """
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Mínimo 8 caracteres',
        }),
        min_length=8,
    )
    confirmar_senha = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repita a senha',
        }),
    )
    is_admin = forms.BooleanField(
        label='Usuário é Administrador?',
        required=False,  # Checkbox não marcado = False (não é obrigatório)
        widget=forms.CheckboxInput(attrs={
            'class': 'h-4 w-4 text-blue-600 rounded',
        }),
        help_text='Administradores podem criar, editar e deletar itens.'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'login do usuário (sem espaços)',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Sobrenome',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@exemplo.com',
            }),
        }
        labels = {
            'username': 'Usuário (login)',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def clean(self):
        """
        Validação personalizada: verifica se as senhas coincidem.
        O método clean() é chamado automaticamente pelo Django na validação.
        """
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirmar = cleaned_data.get('confirmar_senha')

        if senha and confirmar and senha != confirmar:
            # ValidationError exibe o erro no formulário automaticamente
            raise ValidationError({'confirmar_senha': 'As senhas não coincidem.'})

        return cleaned_data

    def save(self, commit=True):
        """
        Salva o usuário com a senha criptografada.
        NUNCA salve senhas em texto puro! O Django cuida da criptografia.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['senha'])  # Criptografa a senha

        # Define se é administrador (staff = acesso ao admin Django)
        if self.cleaned_data.get('is_admin'):
            user.is_staff = True

        if commit:
            user.save()
        return user


# ============================================================
# FORMULÁRIO DE IMPORTAÇÃO DE ARQUIVO
# ============================================================
class ImportacaoForm(forms.Form):
    """
    Formulário para upload de arquivo Excel ou CSV para importação em massa.
    """
    arquivo = forms.FileField(
        label='Arquivo Excel ou CSV',
        widget=forms.FileInput(attrs={
            'class': 'form-input',
            'accept': '.xlsx,.xls,.csv',  # Só aceita esses formatos
        }),
        help_text='Formatos aceitos: .xlsx, .xls, .csv'
    )

    def clean_arquivo(self):
        """
        Valida o arquivo enviado:
        - Verifica se a extensão é permitida
        - Verifica o tamanho máximo (10MB)
        """
        arquivo = self.cleaned_data.get('arquivo')
        if arquivo:
            # Verifica extensão
            nome = arquivo.name.lower()
            if not (nome.endswith('.xlsx') or nome.endswith('.xls') or nome.endswith('.csv')):
                raise ValidationError(
                    'Formato inválido. Use apenas arquivos .xlsx, .xls ou .csv'
                )
            # Verifica tamanho (10MB = 10 * 1024 * 1024 bytes)
            if arquivo.size > 10 * 1024 * 1024:
                raise ValidationError('O arquivo não pode ter mais de 10MB.')
        return arquivo


# ============================================================
# FORMULÁRIO DE BUSCA / FILTRO
# ============================================================
class BuscaPatrimonioForm(forms.Form):
    """
    Formulário de busca e filtragem da lista de patrimônios.
    Todos os campos são opcionais (allow empty).
    """
    busca = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Buscar por nome, chapa ou responsável...',
        })
    )
    status = forms.ChoiceField(
        required=False,
        label='',
        choices=[('', 'Todos os Status')] + PatrimonioItem.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    localizacao = forms.ModelChoiceField(
        required=False,
        label='',
        queryset=Localizacao.objects.all(),
        empty_label='Todas as Localizações',
        widget=forms.Select(attrs={'class': 'form-input'})
    )
