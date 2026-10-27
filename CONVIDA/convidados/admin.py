
from django.contrib import admin

from .models import Convidado, ReservaPresente


@admin.register(Convidado)
class ConvidadoAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'convite',
        'email',
        'telefone',
        'status',
        'numero_acompanhantes',
        'criado_em',
    )

    list_filter = (
        'status',
        'criado_em',
    )

    search_fields = (
        'nome',
        'email',
        'telefone',
        'convite__titulo',
    )

    readonly_fields = (
        'confirmado_em',
        'criado_em',
        'atualizado_em',
    )


@admin.register(ReservaPresente)
class ReservaPresenteAdmin(admin.ModelAdmin):

    list_display = (
        'presente',
        'convidado',
        'status',
        'criado_em',
    )

    list_filter = (
        'status',
        'criado_em',
    )

    search_fields = (
        'presente__nome',
        'convidado__nome',
        'presente__convite__titulo',
    )

    readonly_fields = (
        'criado_em',
        'atualizado_em',
    )

    list_select_related = (
        'presente',
        'convidado',
    )
