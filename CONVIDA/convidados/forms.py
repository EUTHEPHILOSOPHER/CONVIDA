
from django import forms
from .models import Convidado, ReservaPresente




class ConvidadoForm(forms.ModelForm):
    class Meta:
        model = Convidado
        fields = [
            'nome',
            'email',
            'telefone',
            'grau_parentesco',
            'status',
            'numero_acompanhantes',
        ]

        labels = {
            'nome': 'Nome completo',
            'email': 'E-mail',
            'telefone': 'Número de telefone',
            'grau_parentesco': 'Relação com os anfitriões',
            'status': 'Estado da presença',
            'numero_acompanhantes': 'Número de acompanhantes',
        }

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome completo do convidado',
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com',
                'autocomplete': 'email',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de telefone',
                'autocomplete': 'tel',
            }),
            'grau_parentesco': forms.Select(attrs={
                'class': 'form-control',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'numero_acompanhantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 99,
            }),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()

        if len(nome) < 3:
            raise forms.ValidationError(
                'O nome deve ter pelo menos 3 caracteres.'
            )

        return nome



class ConfirmacaoPresencaForm(forms.ModelForm):
    class Meta:
        model = Convidado
        fields = [
            'nome',
            'telefone',
            'email',
            'grau_parentesco',
            'numero_acompanhantes',
            'mensagem',
        ]

        labels = {
            'nome': 'Nome completo',
            'telefone': 'Número de telefone',
            'email': 'E-mail (opcional)',
            'mensagem': 'Mensagem ao casal',
            'grau_parentesco': 'Qual é a tua relação com os anfitriões?',
            'numero_acompanhantes': 'Número de acompanhantes',
        }

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduz o teu nome completo',
                'maxlength': 150,
                'autocomplete': 'name',
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 84 123 4567',
                'maxlength': 30,
                'type': 'tel',
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@email.com (opcional)',
                'autocomplete': 'email',
                'required': False,
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Deixa uma mensagem especial aos noivos...',
                'rows': 4,
                'maxlength': 1000,
            }),
            'grau_parentesco': forms.Select(attrs={
                'class': 'form-control',
            }),
            'numero_acompanhantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 99,
                'required': True,
            }),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()

        if len(nome) < 3:
            raise forms.ValidationError(
                'O nome deve ter pelo menos 3 caracteres.'
            )

        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].strip()

        if len(telefone) < 7:
            raise forms.ValidationError(
                'Introduz um número de telefone válido.'
            )

        return telefone

    def clean_email(self):
        return (self.cleaned_data.get('email') or '').strip()


class ReservaPresenteForm(forms.Form):
    nome = forms.CharField(
        max_length=150,
        min_length=3,
        label='Nome completo',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'O teu nome completo',
            'autocomplete': 'name',
        }),
    )

    telefone = forms.CharField(
        max_length=30,
        min_length=7,
        label='Número de telefone',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ex.: 84 123 4567',
            'autocomplete': 'tel',
        }),
    )

    email = forms.EmailField(
        required=False,
        label='E-mail (opcional)',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail (opcional)',
            'autocomplete': 'email',
        }),
    )

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()

        if len(nome) < 3:
            raise forms.ValidationError(
                'Introduz o teu nome completo.'
            )

        return nome

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone'].strip()

        if len(telefone) < 7:
            raise forms.ValidationError(
                'Introduz um número de telefone válido.'
            )

        return telefone
