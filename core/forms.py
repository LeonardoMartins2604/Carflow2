from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Agendamento, Avaliacao, Contato


class RegistroForm(UserCreationForm):
    """Formulário de Registro de Usuário"""
    nome_completo = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Seu nome completo'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'seu@email.com'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário'
        })
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sua senha'
        })
    )
    password2 = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme sua senha'
        })
    )

    class Meta:
        model = User
        fields = ('nome_completo', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já está cadastrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Este nome de usuário já existe.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('nome_completo')
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    """Formulário de Login"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuário ou Email',
            'autofocus': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Senha'
        })
    )
    lembrar_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


class AgendamentoForm(forms.ModelForm):
    """Formulário de Agendamento de Serviço"""
    data_agendamento = forms.DateTimeField(
        label='Data e Hora',
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'type': 'datetime-local',
            'min': timezone.now().isoformat()
        })
    )

    class Meta:
        model = Agendamento
        fields = [
            'servico',
            'data_agendamento',
            'nome_cliente',
            'email_cliente',
            'telefone_cliente',
            'veiculo',
            'placa_veiculo',
            'observacoes'
        ]
        widgets = {
            'servico': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nome_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo'
            }),
            'email_cliente': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'telefone_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 98765-4321'
            }),
            'veiculo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Toyota Corolla 2020'
            }),
            'placa_veiculo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ABC-1234'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observações adicionais (opcional)'
            })
        }

    def clean_data_agendamento(self):
        data = self.cleaned_data.get('data_agendamento')
        if data and data < timezone.now():
            raise ValidationError('A data do agendamento deve ser no futuro.')
        return data

    def clean_telefone_cliente(self):
        telefone = self.cleaned_data.get('telefone_cliente')
        # Remove caracteres não numéricos
        telefone_limpo = ''.join(filter(str.isdigit, telefone))
        if len(telefone_limpo) < 10:
            raise ValidationError('Telefone inválido.')
        return telefone


class AvaliacaoForm(forms.ModelForm):
    """Formulário de Avaliação de Serviço"""
    class Meta:
        model = Avaliacao
        fields = ['rating', 'comentario']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, f"{i}⭐") for i in range(1, 6)],
                attrs={'class': 'form-check-input'}
            ),
            'comentario': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Deixe seu comentário (opcional)'
            })
        }


class ContatoForm(forms.ModelForm):
    """Formulário de Contato"""
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'assunto', 'mensagem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 98765-4321'
            }),
            'assunto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Assunto da mensagem'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Sua mensagem'
            })
        }


class BuscaProdutoForm(forms.Form):
    """Formulário de Busca de Produtos"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar produto...'
        })
    )
    categoria = forms.ModelChoiceField(
        required=False,
        queryset=None,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    ordenacao = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Ordenar por'),
            ('-criado_em', 'Mais recentes'),
            ('preco', 'Menor preço'),
            ('-preco', 'Maior preço'),
            ('nome', 'Nome A-Z'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        from .models import Categoria
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.all()
