from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CadastroUsuarioForm, LoginUsuarioForm


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
def dashboard(request):

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