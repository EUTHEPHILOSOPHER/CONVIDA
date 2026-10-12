from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ConviteForm
from .models import Convite


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


@login_required
def criar_convite(request):

    if request.method == 'POST':
        tipo_evento = request.POST.get('tipo_evento')

        if tipo_evento:
            return redirect(
                'dados_convite',
                tipo_evento=tipo_evento
            )

    return render(
        request,
        'convites/criar_convite.html'
    )

@login_required
def dados_convite(request, tipo_evento):

    tipos_validos = dict(
        Convite.TIPO_EVENTO_CHOICES
    )

    if tipo_evento not in tipos_validos:
        return redirect('criar_convite')

    templates = [
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

    if request.method == 'POST':

        template = request.POST.get('template')

        templates_validos = [
            item['id']
            for item in templates
        ]

        if template in templates_validos:

            return redirect(
                'dados_evento',
                tipo_evento=tipo_evento,
                template=template
            )

    return render(
        request,
        'convites/dados_convite.html',
        {
            'tipo_evento': tipo_evento,
            'tipo_evento_nome': tipos_validos[tipo_evento],
            'templates': templates,
        }
    )

@login_required
def dados_evento(request, tipo_evento, template):

    tipos_validos = dict(Convite.TIPO_EVENTO_CHOICES)

    templates_validos = {
        'minimal-blue',
        'floral',
        'luxury-gold',
        'tropical',
        'african-heritage',
    }

    if tipo_evento not in tipos_validos:
        return redirect('criar_convite')

    if template not in templates_validos:
        return redirect(
            'dados_convite',
            tipo_evento=tipo_evento,
        )

    if request.method == 'POST':
        form = ConviteForm(request.POST)

        if form.is_valid():
            convite = form.save(commit=False)
            convite.usuario = request.user
            convite.tipo_evento = tipo_evento
            convite.template = template
            convite.status = 'rascunho'
            convite.save()

            return redirect(
                'editar_convite',
                slug=convite.slug,
            )

    else:
        form = ConviteForm(initial={
            'tipo_evento': tipo_evento,
            'template': template,
        })

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



@login_required
def editar_convite(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    if request.method == 'POST':
        form = ConviteForm(request.POST, instance=convite)

        if form.is_valid():
            form.save()
            return redirect('editar_convite', slug=convite.slug)
    else:
        form = ConviteForm(instance=convite)

    return render(
        request,
        'convites/editar_convite.html',
        {
            'form': form,
            'convite': convite,
        },
    )


@login_required
def visualizar_convite(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    return render(
        request,
        'convites/visualizar_convite.html',
        {'convite': convite},
    )


@login_required
def publicar_convite(request, slug):
    if request.method != 'POST':
        return redirect(
            'editar_convite',
            slug=slug,
        )

    convite = get_object_or_404(
        Convite,
        slug=slug,
        usuario=request.user,
    )

    convite.status = 'publicado'
    convite.save(update_fields=['status', 'atualizado_em'])

    return redirect(
        'editar_convite',
        slug=convite.slug,
    )


def convite_publico(request, slug):
    convite = get_object_or_404(
        Convite,
        slug=slug,
        status='publicado',
    )

    return render(
        request,
        'convites/visualizar_convite.html',
        {'convite': convite},
    )
