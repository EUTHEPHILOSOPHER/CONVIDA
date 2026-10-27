from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm, LoginUsuarioForm

from convites.models import Convite
from convidados.models import Convidado


def gerar_username(usuario):

    primeiro_nome = usuario.first_name.strip().lower()
    ultimo_nome = usuario.last_name.strip().lower()

    base = f'{primeiro_nome}.{ultimo_nome}'

    username = base

    contador = 1

    from .models import Usuario

    while Usuario.objects.filter(username=username).exists():

        username = f'{base}{contador}'

        contador += 1

    return username


def cadastro(request):
    if request.method == 'POST':

        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.save(commit=False)

            usuario.username = gerar_username(usuario)

            usuario.save()

            login(request, usuario)

            return redirect('dashboard')

    else:

        form = CadastroUsuarioForm()


    return render(
        request,
        'html/usuarios/cadastro.html',
        {
            'form': form,
        }
    )


@login_required

@login_required
def dashboard(request):
    # Convites do utilizador autenticado
    convites = Convite.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

    # Estatísticas de convites
    total_convites = convites.count()

    total_publicados = convites.filter(
        status='publicado'
    ).count()

    total_rascunhos = convites.filter(
        status='rascunho'
    ).count()

    total_arquivados = convites.filter(
        status='arquivado'
    ).count()

    # Convidados associados aos convites deste utilizador
    convidados = Convidado.objects.filter(
        convite__usuario=request.user
    )

    total_convidados = convidados.count()

    # Respostas dos convidados
    total_confirmacoes = convidados.filter(
        status='confirmado'
    ).count()

    total_pendentes = convidados.filter(
        status='pendente'
    ).count()

    total_recusados = convidados.filter(
        status='recusado'
    ).count()

    # Cinco convites mais recentes
    convites_recentes = convites[:5]

    contexto = {
        'convites': convites,
        'convites_recentes': convites_recentes,

        'total_convites': total_convites,
        'total_publicados': total_publicados,
        'total_rascunhos': total_rascunhos,
        'total_arquivados': total_arquivados,

        'total_convidados': total_convidados,
        'total_confirmacoes': total_confirmacoes,
        'total_pendentes': total_pendentes,
        'total_recusados': total_recusados,
    }

    return render(
        request,
        'html/usuarios/dashboard.html',
        contexto
    )

    # Convites pertencentes ao utilizador autenticado
    convites = Convite.objects.filter(
        usuario=request.user
    ).order_by('-criado_em')

    # Estatísticas reais
    total_convites = convites.count()

    total_publicados = convites.filter(
        status='publicado'
    ).count()

    total_rascunhos = convites.filter(
        status='rascunho'
    ).count()

    total_arquivados = convites.filter(
        status='arquivado'
    ).count()

    # Convites mais recentes para apresentar no dashboard
    convites_recentes = convites[:5]

    contexto = {
        'convites': convites,
        'convites_recentes': convites_recentes,
        'total_convites': total_convites,
        'total_publicados': total_publicados,
        'total_rascunhos': total_rascunhos,
        'total_arquivados': total_arquivados,
    }

    return render(
        request,
        'html/usuarios/dashboard.html',
        contexto
    )

    return render(
        request,
        'html/usuarios/dashboard.html'
    )

def login_usuario(request):

    if request.method == 'POST':

        form = LoginUsuarioForm(request.POST)

        if form.is_valid():

            usuario = form.cleaned_data['usuario']

            login(request, usuario)

            return redirect('dashboard')

    else:

        form = LoginUsuarioForm()

    return render(
        request,
        'html/usuarios/login.html',
        {
            'form': form
        }
    )


def logout_usuario(request):
    logout(request)
    return redirect('login')