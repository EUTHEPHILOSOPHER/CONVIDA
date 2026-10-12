
from django import forms
from .models import Convite


class ConviteForm(forms.ModelForm):

    class Meta:
        model = Convite

        fields = (
            'titulo',
            'tipo_evento',
            'template',
            'data_evento',
            'hora_evento',
            'local_evento',
            'descricao',
        )

        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Casamento de Ana e Cleiton',
            }),
            'tipo_evento': forms.Select(attrs={
                'class': 'form-control',
            }),
            'template': forms.HiddenInput(),
            'data_evento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'hora_evento': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'local_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do local ou endereço',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Escreva uma mensagem para os convidados...',
            }),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo'].strip()

        if len(titulo) < 3:
            raise forms.ValidationError(
                'O título deve ter pelo menos 3 caracteres.'
            )

        return titulo
