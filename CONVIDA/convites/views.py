
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django import forms
from formtools.wizard.views import SessionWizardView
from pathlib import Path
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    ConviteForm,
    PresenteForm,
    LocalEventoForm,
    DadosEventoWizardForm,
    DesignConviteWizardForm,
    MusicaConviteWizardForm,
)
from .models import Convite, Presente, LocalEvento


# ============================================================
# CONFIGURAÇÃO DOS TEMPLATES
# ============================================================

TEMPLATES_CONVITE = [
    {
        'id': 'minimal-blue',
        'nome': 'Minimal Blue',
        'categoria': 'Minimalista',
        'descricao': 'Elegante, limpo e moderno.',
        'classe': 'minimal-blue',
    },
    {
        'id': 'floral',
        'nome': 'Floral',
        'categoria': 'Romântico',
        'descricao': 'Delicado e sofisticado.',
        'classe': 'floral',
    },
    {
        'id': 'luxury-gold',
        'nome': 'Luxury Gold',
        'categoria': 'Luxo',
        'descricao': 'Clássico e sofisticado.',
        'classe': 'luxury-gold',
    },
    {
        'id': 'tropical',
        'nome': 'Tropical',
        'categoria': 'Tropical',
        'descricao': 'Leve, alegre e vibrante.',
        'classe': 'tropical',
    },
    {
        'id': 'african-heritage',
        'nome': 'African Heritage',
        'categoria': 'Cultural',
        'descricao': 'Inspirado na identidade africana.',
        'classe': 'african-heritage',
    },
]

TEMPLATES_VALIDOS = {
    item['id'] for item in TEMPLATES_CONVITE
}


class QuantidadeLocaisWizardForm(forms.Form):
    """Define quantos locais/programações serão adicionados ao convite."""

    numero_locais = forms.IntegerField(
        label="Quantos locais terá o evento?",
        min_value=0,
        max_value=10,
        initial=0,
        help_text="Podes adicionar até 10 locais. Escolhe 0 se não quiseres adicionar locais agora.",
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": 0,
            "max": 10,
        }),
    )


def criar_form_locais_wizard(numero_locais):
    """Cria campos para cada local seleccionado na etapa anterior."""
    campos = {}

    for numero in range(1, numero_locais + 1):
        prefixo = f"local_{numero}_"

        campos[prefixo + "nome"] = forms.CharField(
            label=f"Local {numero} — nome do local",
            max_length=200,
            widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Igreja Central",
            }),
        )
        campos[prefixo + "atividade"] = forms.CharField(
            label="Actividade",
            max_length=200,
            widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Cerimónia religiosa",
            }),
        )
        campos[prefixo + "data"] = forms.DateField(
            label="Data",
            required=False,
            widget=forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
        )
        campos[prefixo + "hora"] = forms.TimeField(
            label="Hora",
            required=False,
            widget=forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),
        )
        campos[prefixo + "localizacao"] = forms.CharField(
            label="Endereço ou localização",
            max_length=255,
            widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex.: Avenida Eduardo Mondlane, Chimoio",
            }),
        )

    return type(
        "LocaisEventoWizardForm",
        (forms.Form,),
        campos,
    )


# ============================================================
# ASSISTENTE DE CRIAÇÃO DE CONVITES (MULTI-ETAPAS)
# ============================================================

class CriarConviteWizard(SessionWizardView):
    """Cria um convite apenas no fim do assistente."""

    form_list = [
        ("evento", DadosEventoWizardForm),
        ("quantidade_locais", QuantidadeLocaisWizardForm),
        ("locais", forms.Form),
        ("design", DesignConviteWizardForm),
        ("musica", MusicaConviteWizardForm),
    ]

    template_name = "convites/criar_convite_wizard.html"

    file_storage = FileSystemStorage(
        location=str(Path(settings.MEDIA_ROOT) / "wizard_uploads")
    )

    def get_form(self, step=None, data=None, files=None):
        step = step or self.steps.current

        if step != "locais":
            return super().get_form(step, data, files)

        dados_quantidade = self.get_cleaned_data_for_step("quantidade_locais") or {}
        numero_locais = dados_quantidade.get("numero_locais", 0)
        FormLocais = criar_form_locais_wizard(numero_locais)

        return FormLocais(
            data=data,
            files=files,
            prefix=self.get_form_prefix(step),
            initial=self.get_form_initial(step),
        )

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == "design":
            initial.setdefault("template", "minimal-blue")
        elif step == "musica":
            initial.setdefault("reproduzir_musica", True)
        return initial

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        context["titulo_pagina"] = "Criar convite"
        context["etapa_atual"] = self.steps.current
        context["total_etapas"] = self.steps.count
        context["templates"] = TEMPLATES_CONVITE
        context["numero_locais"] = (
            (self.get_cleaned_data_for_step("quantidade_locais") or {}).get("numero_locais", 0)
        )
        return context

    def done(self, form_list, **kwargs):
        dados = self.get_all_cleaned_data()
        tipo_evento = dados.get("tipo_evento")
        template = dados.get("template")
        tipos_validos = dict(Convite.TIPO_EVENTO_CHOICES)

        if tipo_evento not in tipos_validos or template not in TEMPLATES_VALIDOS:
            messages.error(
                self.request,
                "Os dados do evento ou o design seleccionado são inválidos. "
                "Por favor, inicia novamente a criação do convite.",
            )
            return redirect("criar_convite")

        convite = Convite(
            usuario=self.request.user,
            titulo=dados["titulo"],
            tipo_evento=tipo_evento,
            template=template,
            data_evento=dados["data_evento"],
            hora_evento=dados["hora_evento"],
            local_evento=dados["local_evento"],
            descricao=dados.get("descricao", ""),
            reproduzir_musica=bool(dados.get("reproduzir_musica", True)),
            status="rascunho",
        )

        musica = dados.get("musica")
        if musica:
            convite.musica = musica

        convite.save()

        dados_locais = self.get_cleaned_data_for_step("locais") or {}
        dados_quantidade = self.get_cleaned_data_for_step("quantidade_locais") or {}
        numero_locais = dados_quantidade.get("numero_locais", 0)

        for numero in range(1, numero_locais + 1):
            prefixo = f"local_{numero}_"
            LocalEvento.objects.create(
                convite=convite,
                nome=dados_locais.get(prefixo + "nome", "").strip(),
                atividade=dados_locais.get(prefixo + "atividade", "").strip(),
                data=dados_locais.get(prefixo + "data"),
                hora=dados_locais.get(prefixo + "hora"),
                localizacao=dados_locais.get(prefixo + "localizacao", "").strip(),
                ordem=numero,
            )

        messages.success(
            self.request,
            "Convite criado com sucesso! Agora podes rever os dados e "
            "personalizar os locais, presentes e restantes detalhes.",
        )
        return redirect("editar_convite", slug=convite.slug)


# ============================================================
# MEUS CONVITES
# ============================================================

@login_required
def meus_convites(request):
    convites = Convite.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

    return render(
        request,
        'convites/meus_convites.html',
        {
            'convites': convites,
        }
    )


# ============================================================
# INICIAR CRIAÇÃO DO CONVITE
# ============================================================

@login_required
def criar_convite(request):
    if request.method == 'POST':
        tipo_evento = request.POST.get('tipo_evento')

        tipos_validos = dict(Convite.TIPO_EVENTO_CHOICES)

        if tipo_evento in tipos_validos:
            return redirect(
                'dados_convite',
                tipo_evento=tipo_evento,
            )

        messages.error(
            request,
            'Seleciona um tipo de evento válido.',
        )

    return render(
        request,
        'convites/criar_convite.html',
    )


# ============================================================
# ESCOLHER TEMPLATE DURANTE A CRIAÇÃO
# ============================================================

@login_required
def dados_convite(request, tipo_evento):
    tipos_validos = dict(Convite.TIPO_EVENTO_CHOICES)

    if tipo_evento not in tipos_validos:
        messages.error(
            request,
            'O tipo de evento selecionado não é válido.',
        )
        return redirect('criar_convite')

    if request.method == 'POST':
        template = request.POST.get('template')

        if template in TEMPLATES_VALIDOS:
            return redirect(
                'dados_evento',
                tipo_evento=tipo_evento,
                template=template,
            )

        messages.error(
            request,
            'Seleciona um template válido.',
        )

    return render(
        request,
        'convites/dados_convite.html',
        {
            'tipo_evento': tipo_evento,
            'tipo_evento_nome': tipos_validos[tipo_evento],
            'templates': TEMPLATES_CONVITE,
        }
    )


# ============================================================
# PREENCHER DADOS E CRIAR CONVITE
# ============================================================

@login_required
def dados_evento(request, tipo_evento, template):
    tipos_validos = dict(Convite.TIPO_EVENTO_CHOICES)

    if tipo_evento not in tipos_validos:
        messages.error(
            request,
            'O tipo de evento não é válido.',
        )
        return redirect('criar_convite')

    if template not in TEMPLATES_VALIDOS:
        messages.error(
            request,
            'O template selecionado não é válido.',
        )
        return redirect(
            'dados_convite',
            tipo_evento=tipo_evento,
        )

    if request.method == 'POST':
        form = ConviteForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            convite = form.save(commit=False)

            convite.usuario = request.user
            convite.tipo_evento = tipo_evento
            convite.template = template
            convite.status = 'rascunho'

            convite.save()

            messages.success(
                request,
                'Rascunho criado. Agora podes personalizar o convite.',
            )

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

    else:
        form = ConviteForm(
            initial={
                'tipo_evento': tipo_evento,
                'template': template,
            }
        )

    return render(
        request,
        'convites/dados_evento.html',
        {
            'form': form,
            'tipo_evento': tipo_evento,
            'tipo_evento_nome': tipos_validos[tipo_evento],
            'template': template,
        },
    )


# ============================================================
# EDITAR CONVITE E ALTERAR TEMPLATE
# ============================================================


@login_required
def editar_convite(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    if request.method == 'POST':
        acao = request.POST.get('acao')

        # ----------------------------------------------------
        # 1. ALTERAR APENAS O TEMPLATE
        # ----------------------------------------------------
        if acao == 'alterar_template':
            novo_template = request.POST.get('novo_template')

            if novo_template not in TEMPLATES_VALIDOS:
                messages.error(
                    request,
                    'O template selecionado não é válido.',
                )
            else:
                convite.template = novo_template
                convite.save(
                    update_fields=['template', 'atualizado_em']
                )

                messages.success(
                    request,
                    'Template do convite atualizado com sucesso.',
                )

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

        # ----------------------------------------------------
        # 2. GUARDAR APENAS AS CONFIGURAÇÕES DE MÚSICA
        # ----------------------------------------------------
        if acao == 'guardar_musica':
            nova_musica = request.FILES.get('musica')

            # A checkbox só envia um valor quando está marcada.
            reproduzir = request.POST.get('reproduzir_musica') == 'on'

            if nova_musica:
                # Validação básica do tipo de ficheiro.
                extensoes_validas = (
                    '.mp3',
                    '.wav',
                    '.ogg',
                    '.m4a',
                    '.aac',
                    '.flac',
                )

                nome_ficheiro = nova_musica.name.lower()

                if not nome_ficheiro.endswith(extensoes_validas):
                    messages.error(
                        request,
                        'Formato de música inválido. '
                        'Utiliza MP3, WAV, OGG, M4A, AAC ou FLAC.',
                    )

                    return redirect(
                        'editar_convite',
                        slug=convite.slug,
                    )

                # O Django substitui o ficheiro associado ao campo.
                # O ficheiro anterior não é eliminado automaticamente
                # em todas as configurações de armazenamento.
                musica_anterior = convite.musica.name

                convite.musica = nova_musica
                convite.reproduzir_musica = reproduzir
                convite.save(
                    update_fields=[
                        'musica',
                        'reproduzir_musica',
                        'atualizado_em',
                    ]
                )

                # Remove o ficheiro anterior quando o nome mudou.
                if (
                    musica_anterior
                    and convite.musica.name != musica_anterior
                ):
                    convite.musica.storage.delete(musica_anterior)

            else:
                # Permite activar/desactivar a reprodução sem
                # carregar novamente o ficheiro de música.
                convite.reproduzir_musica = reproduzir
                convite.save(
                    update_fields=[
                        'reproduzir_musica',
                        'atualizado_em',
                    ]
                )

            messages.success(
                request,
                'Configurações de música guardadas com sucesso.',
            )

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

        # ----------------------------------------------------
        # 3. REMOVER APENAS A MÚSICA
        # ----------------------------------------------------
        if acao == 'remover_musica':
            if convite.musica:
                convite.musica.delete(save=False)

                convite.reproduzir_musica = False
                convite.save(
                    update_fields=[
                        'musica',
                        'reproduzir_musica',
                        'atualizado_em',
                    ]
                )

                messages.success(
                    request,
                    'Música removida do convite com sucesso.',
                )
            else:
                messages.info(
                    request,
                    'Este convite não tem nenhuma música associada.',
                )

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

        # ----------------------------------------------------
        # 4. EDITAR OS DADOS DO EVENTO
        # ----------------------------------------------------
        form = ConviteForm(
            request.POST,
            request.FILES,
            instance=convite,
        )

        if form.is_valid():
            # Preserva os campos que agora são geridos
            # em sessões independentes.
            template_atual = convite.template
            musica_atual = convite.musica
            reproduzir_atual = convite.reproduzir_musica

            convite_atualizado = form.save(commit=False)

            convite_atualizado.template = template_atual
            convite_atualizado.musica = musica_atual
            convite_atualizado.reproduzir_musica = reproduzir_atual

            convite_atualizado.save()

            messages.success(
                request,
                'Dados do convite atualizados com sucesso.',
            )

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

        messages.error(
            request,
            'Não foi possível guardar as alterações. '
            'Verifica os campos assinalados.',
        )

    else:
        form = ConviteForm(instance=convite)

    return render(
        request,
        'convites/editar_convite.html',
        {
            'form': form,
            'convite': convite,
            'templates': TEMPLATES_CONVITE,
        },
    )

# ============================================================
# ELIMINAR CONVITE
# ============================================================

@login_required
@require_POST
def eliminar_convite(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    titulo_convite = convite.titulo
    convite.delete()

    messages.success(
        request,
        f'O convite "{titulo_convite}" foi eliminado com sucesso.',
    )

    return redirect('meus_convites')

# ============================================================
# PRÉ-VISUALIZAÇÃO PRIVADA
# ============================================================

@login_required
def visualizar_convite(request, slug):
    convite = get_object_or_404(
        Convite.objects.prefetch_related(
            'locais',
            'presentes',
        ),
        slug=slug,
        usuario=request.user,
    )

    locais = convite.locais.all().order_by('ordem', 'id')

    presentes = convite.presentes.filter(
        ativo=True,
    )

    return render(
        request,
        'convites/visualizar_convite.html',
        {
            'convite': convite,
            'locais': locais,
            'presentes': presentes,
            'modo_pre_visualizacao': True,
        },
    )



# ============================================================
# PUBLICAR CONVITE
# ============================================================

@login_required
@require_POST
def publicar_convite(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    if convite.status == 'publicado':
        messages.info(
            request,
            'Este convite já está publicado.',
        )
    else:
        convite.status = 'publicado'
        convite.save(
            update_fields=['status', 'atualizado_em']
        )

        messages.success(
            request,
            'Convite publicado com sucesso.',
        )

    return redirect(
        'editar_convite',
        slug=convite.slug,
    )


# ============================================================
# CONVITE PÚBLICO
# ============================================================

def convite_publico(request, slug):
    convite = get_object_or_404(
        Convite.objects.prefetch_related(
            'locais',
            'presentes',
        ),
        slug=slug,
        status='publicado',
    )

    locais = convite.locais.all().order_by('ordem', 'id')

    presentes = convite.presentes.filter(
        ativo=True,
    )

    return render(
        request,
        'convites/visualizar_convite.html',
        {
            'convite': convite,
            'locais': locais,
            'presentes': presentes,
            'modo_pre_visualizacao': False,
        },
    )

# ============================================================
# GERIR PRESENTES
# ============================================================

@login_required
def gerir_presentes(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    presentes = convite.presentes.all()

    return render(
        request,
        'convites/gerir_presentes.html',
        {
            'convite': convite,
            'presentes': presentes,
        },
    )


@login_required
def adicionar_presente(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    if request.method == 'POST':
        form = PresenteForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            presente = form.save(commit=False)
            presente.convite = convite
            presente.save()

            messages.success(
                request,
                'Presente adicionado com sucesso.',
            )

            return redirect(
                'gerir_presentes',
                slug=convite.slug,
            )

    else:
        form = PresenteForm()

    return render(
        request,
        'convites/form_presente.html',
        {
            'convite': convite,
            'form': form,
            'titulo_pagina': 'Adicionar presente',
        },
    )


@login_required
def editar_presente(request, slug, presente_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    presente = get_object_or_404(
        Presente,
        pk=presente_id,
        convite=convite,
    )

    if request.method == 'POST':
        form = PresenteForm(
            request.POST,
            request.FILES,
            instance=presente,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Presente atualizado com sucesso.',
            )

            return redirect(
                'gerir_presentes',
                slug=convite.slug,
            )

    else:
        form = PresenteForm(instance=presente)

    return render(
        request,
        'convites/form_presente.html',
        {
            'convite': convite,
            'form': form,
            'presente': presente,
            'titulo_pagina': 'Editar presente',
        },
    )


@login_required
@require_POST
def remover_presente(request, slug, presente_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    presente = get_object_or_404(
        Presente,
        pk=presente_id,
        convite=convite,
    )

    if presente.reservas.filter(status='reservado').exists():
        messages.error(
            request,
            'Este presente tem reservas ativas. '
            'Cancele ou resolva as reservas antes de o remover.',
        )
    else:
        presente.delete()

        messages.success(
            request,
            'Presente removido com sucesso.',
        )

    return redirect(
        'gerir_presentes',
        slug=convite.slug,
    )


# ============================================================
# GERIR LOCAIS E PROGRAMAÇÃO
# ============================================================

@login_required
def gerir_locais(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    locais = convite.locais.all()

    return render(
        request,
        'convites/gerir_locais.html',
        {
            'convite': convite,
            'locais': locais,
        },
    )


@login_required
def adicionar_local(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    if request.method == 'POST':
        form = LocalEventoForm(request.POST)

        if form.is_valid():
            local = form.save(commit=False)
            local.convite = convite
            local.save()

            messages.success(
                request,
                'Local do evento adicionado com sucesso.',
            )

            return redirect(
                'gerir_locais',
                slug=convite.slug,
            )

    else:
        form = LocalEventoForm(
            initial={
                'ordem': convite.locais.count() + 1,
            }
        )

    return render(
        request,
        'convites/form_local.html',
        {
            'convite': convite,
            'form': form,
            'titulo_pagina': 'Adicionar local',
        },
    )


@login_required
def editar_local(request, slug, local_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    local = get_object_or_404(
        LocalEvento,
        pk=local_id,
        convite=convite,
    )

    if request.method == 'POST':
        form = LocalEventoForm(
            request.POST,
            instance=local,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Local do evento atualizado com sucesso.',
            )

            return redirect(
                'gerir_locais',
                slug=convite.slug,
            )

    else:
        form = LocalEventoForm(instance=local)

    return render(
        request,
        'convites/form_local.html',
        {
            'convite': convite,
            'form': form,
            'local': local,
            'titulo_pagina': 'Editar local',
        },
    )


@login_required
@require_POST
def remover_local(request, slug, local_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    local = get_object_or_404(
        LocalEvento,
        pk=local_id,
        convite=convite,
    )

    local.delete()

    messages.success(
        request,
        'Local do evento removido com sucesso.',
    )

    return redirect(
        'gerir_locais',
        slug=convite.slug,
    )
