from django.urls import path
from . import views

app_name = 'convidados'

urlpatterns = [
    path(
        'convites/<slug:slug>/convidados/',
        views.lista_convidados,
        name='lista_convidados',
    ),
    path(
        'convite/<slug:slug>/convidados/adicionar/',
        views.criar_convidado,
        name='criar_convidado',
    ),
    path(
        'convite/<slug:slug>/convidados/<int:convidado_id>/editar/',
        views.editar_convidado,
        name='editar_convidado',
    ),
    path(
        'convite/<slug:slug>/convidados/<int:convidado_id>/remover/',
        views.remover_convidado,
        name='remover_convidado',
    ),

    path(
    'convites/p/<slug:slug>/confirmar/',
    views.confirmar_presenca,
    name='confirmar_presenca',
    ),
    path(
    'convites/<slug:slug>/convidados/<int:convidado_id>/aceitar/',
    views.aceitar_presenca,
    name='aceitar_presenca',
    ),
    path(
        'convites/<slug:slug>/convidados/<int:convidado_id>/rejeitar/',
        views.rejeitar_presenca,
        name='rejeitar_presenca',
    ),
    path(
    'convites/p/<slug:slug>/presentes/<int:presente_id>/reservar/',
    views.reservar_presente,
    name='reservar_presente',
    ),
    path(
        'convites/',
        views.escolher_convite_convidados,
        name='escolher_convite_convidados',
    ),
]
