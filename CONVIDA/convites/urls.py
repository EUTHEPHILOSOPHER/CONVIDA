
from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views


urlpatterns = [

    # ============================================================
    # LISTAGEM E CRIAÇÃO DE CONVITES
    # ============================================================

    path(
        '',
        views.meus_convites,
        name='meus_convites',
    ),

    # Assistente de criação em várias etapas
    path(
        'criar/assistente/',
        login_required(
            views.CriarConviteWizard.as_view(
                views.CriarConviteWizard.form_list
            )
        ),
        name='criar_convite_wizard',
    ),

    # Rotas antigas — mantidas para não quebrar funcionalidades
    path(
        'criar/',
        views.criar_convite,
        name='criar_convite',
    ),

    path(
        '<slug:slug>/eliminar/',
        views.eliminar_convite,
        name='eliminar_convite',
    ),

    path(
        'criar/<slug:tipo_evento>/',
        views.dados_convite,
        name='dados_convite',
    ),

    path(
        'criar/<slug:tipo_evento>/<slug:template>/',
        views.dados_evento,
        name='dados_evento',
    ),

    # ============================================================
    # EDIÇÃO, VISUALIZAÇÃO E PUBLICAÇÃO
    # ============================================================

    path(
        '<slug:slug>/editar/',
        views.editar_convite,
        name='editar_convite',
    ),

    path(
        '<slug:slug>/visualizar/',
        views.visualizar_convite,
        name='visualizar_convite',
    ),

    path(
        '<slug:slug>/publicar/',
        views.publicar_convite,
        name='publicar_convite',
    ),

    path(
        'p/<slug:slug>/',
        views.convite_publico,
        name='convite_publico',
    ),

    # ============================================================
    # GESTÃO DE PRESENTES
    # ============================================================

    path(
        '<slug:slug>/presentes/',
        views.gerir_presentes,
        name='gerir_presentes',
    ),

    path(
        '<slug:slug>/presentes/adicionar/',
        views.adicionar_presente,
        name='adicionar_presente',
    ),

    path(
        '<slug:slug>/presentes/<int:presente_id>/editar/',
        views.editar_presente,
        name='editar_presente',
    ),

    path(
        '<slug:slug>/presentes/<int:presente_id>/remover/',
        views.remover_presente,
        name='remover_presente',
    ),

    # ============================================================
    # GESTÃO DE LOCAIS E PROGRAMAÇÃO
    # ============================================================

    path(
        '<slug:slug>/locais/',
        views.gerir_locais,
        name='gerir_locais',
    ),

    path(
        '<slug:slug>/locais/adicionar/',
        views.adicionar_local,
        name='adicionar_local',
    ),

    path(
        '<slug:slug>/locais/<int:local_id>/editar/',
        views.editar_local,
        name='editar_local',
    ),

    path(
        '<slug:slug>/locais/<int:local_id>/remover/',
        views.remover_local,
        name='remover_local',
    ),
]
