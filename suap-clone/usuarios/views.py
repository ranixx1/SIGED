from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# View para cadastro de usuários
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        # Validações básicas
        if senha != confirmar_senha:
            messages.error(request, 'Senha e confirmar senha devem ser iguais')
            return redirect('/usuarios/cadastro/')

        if len(senha) < 6:
            messages.error(request, 'A senha deve ter 6 ou mais caracteres')
            return redirect('/usuarios/cadastro/')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Já existe um usuário com esse username.')
            return redirect('/usuarios/cadastro/')

        # Criação do usuário
        User.objects.create_user(username=username, password=senha)
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('/usuarios/login/')

# View para login de usuários
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        # Autenticação do usuário
        user = authenticate(request, username=username, password=senha)
        if user is not None:
            auth_login(request, user)
            return redirect('/home/')

        messages.error(request, 'Username ou senha inválidos')
        return redirect('/usuarios/login/')

# View para logout de usuários
def logout(request):
    auth_logout(request)
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('/usuarios/login/')