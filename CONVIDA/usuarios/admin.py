from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'telefone',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'telefone',
    )

    list_filter = (
        'is_staff',
        'is_active',
        'is_superuser',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Informações adicionais',
            {
                'fields': (
                    'telefone',
                    'foto',
                    'data_cadastro',
                    'atualizado_em',
                )
            }
        ),
    )

    readonly_fields = (
        'data_cadastro',
        'atualizado_em',
    )