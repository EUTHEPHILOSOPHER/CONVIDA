from django.contrib import admin

from .models import Convite


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

    ordering = (
        '-criado_em',
    )