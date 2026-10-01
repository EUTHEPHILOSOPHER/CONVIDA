from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import Usuario


class CadastroUsuarioForm(UserCreationForm):

    class Meta:
        model = Usuario

        fields = (
            'first_name',
            'last_name',
            'email',
            'telefone',
            'password1',
            'password2',
        )

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Primeiro nome',
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Apelido',
                }
            ),

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Nome de usuário',
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'seu@email.com',
                }
            ),

            'telefone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+258 84 000 0000',
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme sua senha',
        })

class LoginUsuarioForm(forms.Form):

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'seu@email.com',
                'autocomplete': 'email',
            }
        )
    )

    password = forms.CharField(
        label='Palavra-passe',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite sua palavra-passe',
                'autocomplete': 'current-password',
            }
        )
    )

    lembrar_me = forms.BooleanField(
        required=False,
        label='Lembrar-me'
    )

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            return cleaned_data

        try:

            usuario = Usuario.objects.get(
                email__iexact=email
            )

        except Usuario.DoesNotExist:

            raise forms.ValidationError(
                'Email ou palavra-passe incorretos.'
            )

        usuario = authenticate(
            username=usuario.username,
            password=password
        )

        if usuario is None:

            raise forms.ValidationError(
                'Email ou palavra-passe incorretos.'
            )

        if not usuario.is_active:

            raise forms.ValidationError(
                'Esta conta está desativada.'
            )

        cleaned_data['usuario'] = usuario

        return cleaned_data