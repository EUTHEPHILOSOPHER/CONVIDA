
from django.contrib import admin

from .models import Convite, Presente


@admin.register(Convite)
class ConviteAdmin(admin.ModelAdmin):

    list_display = (
        'titulo',
        'usuario',
        'tipo_evento',
        'data_evento',
        'template',
        'status',
        'criado_em',
    )

    list_filter = (
        'tipo_evento',
        'status',
        'template',
        'criado_em',
    )

    search_fields = (
        'titulo',
        'usuario__first_name',
        'usuario__last_name',
        'usuario__email',
    )

    readonly_fields = (
        'slug',
        'criado_em',
        'atualizado_em',
    )

    ordering = ('-criado_em',)


@admin.register(Presente)
class PresenteAdmin(admin.ModelAdmin):

    list_display = (
        'nome',
        'convite',
        'quantidade',
        'ativo',
        'criado_em',
    )

    list_filter = (
        'ativo',
        'criado_em',
    )

    search_fields = (
        'nome',
        'convite__titulo',
        'convite__usuario__email',
    )

    readonly_fields = (
        'criado_em',
        'atualizado_em',
    )

    list_select_related = ('convite',)
