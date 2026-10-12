from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.meus_convites,
        name='meus_convites'
    ),

    path(
        'criar/',
        views.criar_convite,
        name='criar_convite'
    ),

    path(
        'criar/<slug:tipo_evento>/',
        views.dados_convite,
        name='dados_convite'
    ),

    path(
        'criar/<slug:tipo_evento>/<slug:template>/',
        views.dados_evento,
        name='dados_evento'
    ),

    path(
        '<slug:slug>/editar/',
        views.editar_convite,
        name='editar_convite'
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


]