
from django import forms

from .models import Convite, Presente, LocalEvento


# ============================================================
# SESSÃO 1: DADOS DO EVENTO
# ============================================================

class DadosEventoWizardForm(forms.ModelForm):
    class Meta:
        model = Convite
        fields = (
            'titulo',
            'tipo_evento',
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
        titulo = (self.cleaned_data.get('titulo') or '').strip()

        if len(titulo) < 3:
            raise forms.ValidationError(
                'O título deve ter pelo menos 3 caracteres.'
            )

        return titulo


# ============================================================
# SESSÃO 2: DESIGN DO CONVITE
# ============================================================

class DesignConviteWizardForm(forms.Form):
    template = forms.ChoiceField(
        label='Escolha o design do convite',
        choices=(
            ('minimal-blue', 'Minimal Blue'),
            ('floral', 'Floral'),
            ('luxury-gold', 'Luxury Gold'),
            ('tropical', 'Tropical'),
            ('african-heritage', 'African Heritage'),
        ),
        widget=forms.RadioSelect(),
        initial='minimal-blue',
    )


# ============================================================
# SESSÃO 3: MÚSICA DO CONVITE
# ============================================================

class MusicaConviteWizardForm(forms.Form):
    musica = forms.FileField(
        label='Ficheiro de música',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.mp3,.wav,.ogg,.m4a,.aac,.flac,audio/*',
        }),
        help_text=(
            'Formatos aceites: MP3, WAV, OGG, M4A, AAC e FLAC. '
            'A música é opcional.'
        ),
    )

    reproduzir_musica = forms.BooleanField(
        label='Disponibilizar música no convite público',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
        }),
    )

    def clean_musica(self):
        musica = self.cleaned_data.get('musica')

        if not musica:
            return musica

        extensoes_validas = (
            '.mp3',
            '.wav',
            '.ogg',
            '.m4a',
            '.aac',
            '.flac',
        )

        nome = musica.name.lower()

        if not nome.endswith(extensoes_validas):
            raise forms.ValidationError(
                'Formato inválido. Utiliza MP3, WAV, OGG, M4A, AAC ou FLAC.'
            )

        # Limite inicial de 15 MB para o ficheiro de música.
        limite_bytes = 15 * 1024 * 1024

        if musica.size > limite_bytes:
            raise forms.ValidationError(
                'A música não pode ultrapassar 15 MB.'
            )

        return musica


# ============================================================
# FORMULÁRIO COMPLETO DO CONVITE
# Mantido para edição e compatibilidade com as views actuais.
# ============================================================

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
            'musica',
            'reproduzir_musica',
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

            'musica': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.mp3,.wav,.ogg,.m4a,.aac,.flac,audio/*',
            }),

            'reproduzir_musica': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_titulo(self):
        titulo = (self.cleaned_data.get('titulo') or '').strip()

        if len(titulo) < 3:
            raise forms.ValidationError(
                'O título deve ter pelo menos 3 caracteres.'
            )

        return titulo


# ============================================================
# FORMULÁRIO DE PRESENTES
# ============================================================

class PresenteForm(forms.ModelForm):
    class Meta:
        model = Presente

        fields = (
            'nome',
            'descricao',
            'imagem',
            'quantidade',
            'link_compra',
            'ativo',
        )

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Jogo de panelas',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição do presente (opcional)',
            }),

            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),

            'quantidade': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),

            'link_compra': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...',
            }),

            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome') or '').strip()

        if len(nome) < 2:
            raise forms.ValidationError(
                'O nome do presente deve ter pelo menos 2 caracteres.'
            )

        return nome

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')

        if quantidade is None or quantidade < 1:
            raise forms.ValidationError(
                'A quantidade deve ser pelo menos 1.'
            )

        return quantidade


# ============================================================
# FORMULÁRIO DE LOCAIS E PROGRAMAÇÃO
# ============================================================

class LocalEventoForm(forms.ModelForm):
    class Meta:
        model = LocalEvento

        fields = (
            'nome',
            'atividade',
            'data',
            'hora',
            'localizacao',
            'ordem',
        )

        labels = {
            'nome': 'Nome do local',
            'atividade': 'Actividade',
            'data': 'Data',
            'hora': 'Hora',
            'localizacao': 'Endereço ou localização',
            'ordem': 'Ordem de apresentação',
        }

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Igreja Central',
            }),

            'atividade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Cerimónia religiosa',
            }),

            'data': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'hora': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),

            'localizacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Avenida Eduardo Mondlane, Chimoio',
            }),

            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
            }),
        }

    def clean_nome(self):
        nome = (self.cleaned_data.get('nome') or '').strip()

        if len(nome) < 2:
            raise forms.ValidationError(
                'O nome do local deve ter pelo menos 2 caracteres.'
            )

        return nome

    def clean_atividade(self):
        atividade = (
            self.cleaned_data.get('atividade') or ''
        ).strip()

        if len(atividade) < 2:
            raise forms.ValidationError(
                'A actividade deve ter pelo menos 2 caracteres.'
            )

        return atividade

    def clean_localizacao(self):
        localizacao = (
            self.cleaned_data.get('localizacao') or ''
        ).strip()

        if len(localizacao) < 3:
            raise forms.ValidationError(
                'Indica uma localização válida.'
            )

        return localizacao
