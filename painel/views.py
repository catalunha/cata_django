from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


from datetime import date,timedelta,datetime,timezone

from painel.forms import LoginForm
from painel.models import User
from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Teste
from tarefa.models import Avaliacao,Questao,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicada
from instituicao.models import Instituicao,Conhecimento,Turma

def index(request):
    if request.method == 'POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            if user.cargo == 'aluno':
                return HttpResponseRedirect(reverse('aluno:atuais'))
            elif user.cargo == 'professor':
                return HttpResponseRedirect(reverse('professor:acoes'))
            else:
                return HttpResponseRedirect(reverse('painel:index'))
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'painel/index.html', context)

@login_required
def sair(request):
    logout(request)
    return HttpResponseRedirect(reverse('painel:index'))

@login_required
def alunonovo(request,id):
    if request.method == 'POST':
        novos = request.POST.get('novosalunos')
        linhas=novos.strip().split('\n')
        for linha in linhas :
            novo=linha.strip().split(' ',1)
            # print("{}:{}".format(novo[0],novo[1]))
            if User.objects.filter(username=novo[0]).exists():
                usuario = User.objects.get(username=novo[0])
            else:
                usuario=User.objects.create_user(novo[0], password='abc12345678abc')
                usuario.last_name=novo[1]
                usuario.cargo='aluno'
            usuario.professor.add(request.user)
            usuario.save()
            turma=Turma.objects.get(id=id)
            turma.alunos.add(usuario)
            turma.save()
        return HttpResponseRedirect(reverse('professor:conhecimento'))
    context={'id':id}
    return render(request, 'painel/alunonovo.html', context)


@login_required
def alunoeditar(request,id):
    turma=Turma.objects.get(id=id)
    alunos=turma.alunos.all()
    if request.method == 'POST':
        alunos = request.POST.getlist('alunos')
        for aluno in alunos :
            User.objects.get(id=aluno).delete()
        desativados = request.POST.getlist('desativados')
        User.objects.all().update(is_active=True)
        for desativado in desativados :
            # print(desativado)
            user=User.objects.get(id=desativado)
            # print(user)
            # print(user.is_active)
            user.is_active=False
            user.save()
            # print(user.is_active)
        return HttpResponseRedirect(reverse('professor:conhecimento'))
    context = {'alunos':alunos,'id':id}
    return render(request, 'painel/alunoeditar.html', context)

@login_required
def senhanova(request):
    usuario=request.user
    usuario.set_password('abc12345678abc')
    usuario.save()
    return HttpResponseRedirect(reverse('painel:index'))



@login_required
def senhareset(request,id):
    aluno=User.objects.get(id=id)
    aluno.set_password('abc12345678abc')
    aluno.save()
    return HttpResponseRedirect(reverse('professor:conhecimento'))
