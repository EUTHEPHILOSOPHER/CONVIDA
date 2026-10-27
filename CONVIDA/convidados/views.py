from .forms import ConfirmacaoPresencaForm, ConvidadoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from django.db import transaction

from convites.models import Convite, Presente
from .models import Convidado, ReservaPresente
from .forms import ReservaPresenteForm

def obter_convite_do_utilizador(slug, utilizador):
    return get_object_or_404(
        Convite,
        slug=slug,
        usuario=utilizador,
    )


@login_required
def lista_convidados(request, slug):
    convite = obter_convite_do_utilizador(slug, request.user)
    convidados = convite.convidados.all()

    contexto = {
        'convite': convite,
        'convidados': convidados,
        'total_convidados': convidados.count(),
        'total_confirmados': convidados.filter(
            status='confirmado'
        ).count(),
        'total_pendentes': convidados.filter(
            status='pendente'
        ).count(),
        'total_recusados': convidados.filter(
            status='recusado'
        ).count(),
    }

    return render(
        request,
        'convidados/lista_convidados.html',
        contexto,
    )


@login_required
def criar_convidado(request, slug):
    convite = obter_convite_do_utilizador(slug, request.user)

    if request.method == 'POST':
        form = ConvidadoForm(request.POST)

        if form.is_valid():
            convidado = form.save(commit=False)
            convidado.convite = convite
            convidado.save()

            messages.success(
                request,
                'Convidado adicionado com sucesso.',
            )

            return redirect(
            'convidados:lista_convidados',
            slug=convite.slug,
        )
    else:
        form = ConvidadoForm()

    return render(
        request,
        'convidados/form_convidado.html',
        {
            'form': form,
            'convite': convite,
            'titulo_pagina': 'Adicionar convidado',
        },
    )


@login_required
def editar_convidado(request, slug, convidado_id):
    convite = obter_convite_do_utilizador(slug, request.user)

    convidado = get_object_or_404(
        Convidado,
        pk=convidado_id,
        convite=convite,
    )

    if request.method == 'POST':
        form = ConvidadoForm(
            request.POST,
            instance=convidado,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Dados do convidado atualizados.',
            )

            return redirect(
            'convidados:lista_convidados',
            slug=convite.slug,
        )
    else:
        form = ConvidadoForm(instance=convidado)

    return render(
        request,
        'convidados/form_convidado.html',
        {
            'form': form,
            'convite': convite,
            'convidado': convidado,
            'titulo_pagina': 'Editar convidado',
        },
    )


@login_required
@require_POST
def remover_convidado(request, slug, convidado_id):
    convite = obter_convite_do_utilizador(slug, request.user)

    convidado = get_object_or_404(
        Convidado,
        pk=convidado_id,
        convite=convite,
    )

    convidado.delete()

    messages.success(
        request,
        'Convidado removido com sucesso.',
    )

    return redirect(
    'convidados:lista_convidados',
    slug=convite.slug,
)

@require_POST

@require_POST
def confirmar_presenca(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        status='publicado',
    )

    form = ConfirmacaoPresencaForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            'Não foi possível enviar o pedido. '
            'Verifica os teus dados.',
        )
        return redirect('convite_publico', slug=convite.slug)

    ids_presentes = request.POST.getlist('presentes')

    telefone = ''.join(
        form.cleaned_data['telefone'].split()
    )

    try:
        with transaction.atomic():
            presentes = list(
                Presente.objects.select_for_update().filter(
                    convite=convite,
                    ativo=True,
                    pk__in=ids_presentes,
                )
            )

            # Confirmar que todos os presentes selecionados
            # pertencem ao convite e estão disponíveis.
            if len(presentes) != len(set(ids_presentes)):
                messages.error(
                    request,
                    'Um dos presentes selecionados não está disponível. '
                    'Atualiza a página e tenta novamente.',
                )
                return redirect(
                    'convite_publico',
                    slug=convite.slug,
                )

            for presente in presentes:
                total_reservado = presente.reservas.filter(
                    status='reservado',
                ).count()

                if total_reservado >= presente.quantidade:
                    messages.error(
                        request,
                        f'O presente "{presente.nome}" já não tem '
                        'unidades disponíveis. Escolhe outros presentes.',
                    )
                    return redirect(
                        'convite_publico',
                        slug=convite.slug,
                    )

                reserva_existente = presente.reservas.filter(
                    status='reservado',
                    telefone_reservante=telefone,
                ).exists()

                if reserva_existente:
                    messages.error(
                        request,
                        f'Já existe uma reserva de "{presente.nome}" '
                        'associada a este número de telefone.',
                    )
                    return redirect(
                        'convite_publico',
                        slug=convite.slug,
                    )

            # Criar o convidado apenas depois de validar
            # todos os presentes selecionados.
            convidado = form.save(commit=False)
            convidado.convite = convite
            convidado.status = 'pendente'
            convidado.numero_acompanhantes = 0
            convidado.numero_acompanhantes = form.cleaned_data.get(
                'numero_acompanhantes',
                0,
            )
            convidado.save()

            # Associar cada presente ao mesmo convidado.
            for presente in presentes:
                ReservaPresente.objects.create(
                    presente=presente,
                    convidado=convidado,
                    nome_reservante=convidado.nome,
                    telefone_reservante=telefone,
                    email_reservante=convidado.email,
                    status='reservado',
                )

    except Exception:
        messages.error(
            request,
            'Ocorreu um erro ao enviar o pedido. '
            'Verifica os dados e tenta novamente.',
        )
        return redirect('convite_publico', slug=convite.slug)

    if presentes:
        messages.success(
            request,
            'O pedido de presença e a seleção de presentes '
            'foram enviados com sucesso. Aguarda a aprovação do anfitrião.',
        )
    else:
        messages.success(
            request,
            'O teu pedido de presença foi enviado com sucesso. '
            'Aguarda a aprovação do anfitrião.',
        )

    return redirect('convite_publico', slug=convite.slug)


@login_required
@require_POST
def aceitar_presenca(request, slug, convidado_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    convidado = get_object_or_404(
        Convidado,
        pk=convidado_id,
        convite=convite,
    )

    if convidado.status != 'pendente':
        messages.warning(
            request,
            'Este pedido já foi analisado.',
        )
    else:
        convidado.status = 'confirmado'
        convidado.save()

        messages.success(
            request,
            f'A presença de {convidado.nome} foi aceite.',
        )

    return redirect(
        'convidados:lista_convidados',
        slug=convite.slug,
    )


@login_required
@require_POST
def rejeitar_presenca(request, slug, convidado_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    convidado = get_object_or_404(
        Convidado,
        pk=convidado_id,
        convite=convite,
    )

    if convidado.status != 'pendente':
        messages.warning(
            request,
            'Este pedido já foi analisado.',
        )
    else:
        convidado.status = 'recusado'
        convidado.save()

        messages.success(
            request,
            f'O pedido de {convidado.nome} foi rejeitado.',
        )

    return redirect(
        'convidados:lista_convidados',
        slug=convite.slug,
    )


@require_POST
def reservar_presente(request, slug, presente_id):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        status='publicado',
    )

    form = ReservaPresenteForm(request.POST)

    if not form.is_valid():
        messages.error(
            request,
            'Verifica o teu nome e número de telefone.',
        )
        return redirect(
            'convite_publico',
            slug=convite.slug,
        )

    nome = form.cleaned_data['nome'].strip()
    telefone = ''.join(
        form.cleaned_data['telefone'].split()
    )
    email = form.cleaned_data.get('email', '').strip()

    with transaction.atomic():
        presente = get_object_or_404(
            Presente.objects.select_for_update(),
            pk=presente_id,
            convite=convite,
            ativo=True,
        )

        # Impedir que o mesmo telefone reserve novamente
        # o mesmo presente enquanto existir uma reserva ativa.
        reserva_existente = presente.reservas.filter(
            status='reservado',
            telefone_reservante=telefone,
        ).exists()

        if reserva_existente:
            messages.warning(
                request,
                'Já existe uma reserva deste presente '
                'associada a este número de telefone.',
            )
        else:
            total_reservado = presente.reservas.filter(
                status='reservado',
            ).count()

            if total_reservado >= presente.quantidade:
                messages.error(
                    request,
                    'Este presente já não tem unidades disponíveis.',
                )
            else:
                ReservaPresente.objects.create(
                    presente=presente,
                    nome_reservante=nome,
                    telefone_reservante=telefone,
                    email_reservante=email,
                    status='reservado',
                )

                messages.success(
                    request,
                    'O presente foi reservado com sucesso. '
                    'Obrigado pela tua generosidade!',
                )

    return redirect(
        'convite_publico',
        slug=convite.slug,
    )

@login_required
def escolher_convite_convidados(request):
    convites = Convite.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

    return render(
        request,
        'convidados/escolher_convite.html',
        {
            'convites': convites,
        },
    )

