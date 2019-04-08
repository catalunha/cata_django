from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date,timedelta,datetime,timezone
from django.conf import settings

import os

from painel.models import User,Variavel
from professor.models import Ementa
from professor.forms import EmentaForm
from instituicao.models import Conhecimento,Turma
from situacao.models import Indice,Problema

@login_required
def ementa(request):
    usuario = request.user
    turmas=usuario.na_turma.all()
    ementas=[]
    for turma in turmas :
        ementa=Ementa.objects.filter(conhecimento=turma.conhecimento)
        if ementa :
            ementas.append(ementa[0].texto_md)

    context = {'ementas':ementas,}
    return render(request, 'professor/ementa.html', context)

@login_required
def ementaeditar(request,id):
    conhecimento=Conhecimento.objects.get(id=id)
    ementa=Ementa.objects.get(conhecimento=conhecimento)
    if request.method == 'POST':
        form=EmentaForm(request.POST,instance=ementa)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form = EmentaForm(instance=ementa)
    context = {'form':form,'id':id,'ementa':ementa.texto_md}
    return render(request, 'professor/ementaeditar.html', context)


@login_required
def acoes(request):
    context = {}
    return render(request, 'professor/acoes.html', context)


@login_required
def conhecimento(request):
    usuario = request.user
    conhecimentos=Conhecimento.objects.filter(usuario=usuario).order_by('-ativo','instituicao__nome','nome')
    context = {'conhecimentos':conhecimentos}
    return render(request, 'professor/conhecimento.html', context)

@login_required
def alunotarefas(request,idturma,idaluno):
    turma=Turma.objects.get(id=idturma)
    aluno=User.objects.get(id=idaluno)
    context = {'turma':turma,'aluno':aluno}
    return render(request, 'professor/alunotarefas.html', context)


@login_required
def indice(request):
    usuario = request.user
    conhecimentos=Conhecimento.objects.filter(usuario=usuario,ativo=True).order_by('-ativo','instituicao__nome','nome')
    indices=Indice.objects.filter(conhecimento__in=conhecimentos)

    context = {'conhecimentos':conhecimentos,'indices':indices}
    return render(request, 'professor/indice.html', context)





@login_required
def notas(request):
    usuario = request.user
    conhecimentos=Conhecimento.objects.filter(usuario=usuario,ativo=True).order_by('-ativo','instituicao__nome','nome')

    notaporaluno=[]
    for conhecimento in conhecimentos:
        for turma in conhecimento.turmas.all():
            for aluno in turma.alunos.all():
                linha=[]
                linha.append(conhecimento.instituicao.nome)
                linha.append(conhecimento.usuario.last_name)
                linha.append(conhecimento.nome)
                linha.append(turma.nome)
                linha.append(aluno.last_name)
                linha.append(aluno.username)
                total=0
                numquestoes=0
                for aplicada in aluno.aplicadas_usuario.all() :
                    if aplicada.ativo and aplicada.questao.ativo and aplicada.questao.problema.ativo and aplicada.questao.avaliacao.ativo and aplicada.questao.avaliacao.turma.id == turma.id :
                        numquestoes += 1
                        total = total + aplicada.questao.avaliacao.nota*aplicada.questao.nota*(aplicada.get_total_solucao()+aplicada.get_total_relatorio()+aplicada.get_total_anexo())
                for aplicado in aluno.aplicados_usuario.all() :
                    if aplicado.ativo and aplicado.algoritmo.ativo and aplicado.algoritmo.programa.ativo and aplicado.algoritmo.avaliacao.ativo and aplicado.algoritmo.avaliacao.turma.id == turma.id :
                        numquestoes += 1
                        total = total + aplicado.algoritmo.avaliacao.nota*aplicado.algoritmo.nota*aplicado.get_total_codigo()
                linha.append(numquestoes)
                linha.append(total)
                notaporaluno.append(linha)
    # # print(notaporaluno)

    context = {'conhecimentos':conhecimentos,'notaporaluno':notaporaluno}
    return render(request, 'professor/notas.html', context)
