from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse

import threading

from django.conf import settings
import os
from os import kill
from subprocess import PIPE, Popen

from datetime import date,timedelta,datetime,timezone
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import random

from instituicao.models import Instituicao,Conhecimento,Turma
from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Codigo,Aplicado
from tarefa.forms import AvaliacaoForm,QuestaoForm,AlgoritmoForm
from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Teste
from professor.models import QuestaoStatus,AlgoritmoStatus
from painel.models import User


@login_required
def avaliacaonovo(request,id):
    if request.method == 'POST':
        form=AvaliacaoForm(request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.turma=Turma.objects.get(id=id)
            novo.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form=AvaliacaoForm()
    context = {'form':form,'id':id}
    return render(request, 'tarefa/avaliacaonovo.html', context)

@login_required
def avaliacaoeditar(request,id):
    avaliacao=Avaliacao.objects.get(id=id)
    if request.method == 'POST':
        form=AvaliacaoForm(request.POST,instance=avaliacao)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form = AvaliacaoForm(instance=avaliacao)
    context = {'form':form,'id':avaliacao.id,'tempo':avaliacao}
    return render(request, 'tarefa/avaliacaoeditar.html', context)


@login_required
def avaliacaoaplicar1(request,id):
    avaliacao=Avaliacao.objects.get(id=id)
    alunos=avaliacao.turma.alunos.all()
    context = {'alunos':alunos,'avaliacao':avaliacao,'id':id}
    return render(request, 'tarefa/avaliacaoaplicar1.html', context)


def aplicar(alunos, avaliacao):
    for questao in avaliacao.questoes.all() :
        lista=questao.problema.simulacoes.all()
        for idaluno in alunos :
            aluno=User.objects.get(id=idaluno)
            if not Aplicada.objects.filter(usuario=aluno,questao=questao).exists():
                aplicada,criado = Aplicada.objects.get_or_create(usuario=aluno,questao=questao)
                status,criado = QuestaoStatus.objects.get_or_create(aplicada=aplicada)
                if lista:
                    simulacao=random.choice(lista)
                    for resposta in simulacao.respostas.all() :
                        solucao,criado = Solucao.objects.get_or_create(aplicada=aplicada,resposta=resposta)
                    for texto in simulacao.textos.all() :
                        relatorio,criado = Relatorio.objects.get_or_create(aplicada=aplicada,texto=texto)
                    for arquivo in simulacao.arquivos.all() :
                        anexo,criado = Anexo.objects.get_or_create(aplicada=aplicada,arquivo=arquivo)
                else:
                    context={}
                    return render(request, 'tarefa/avaliacaoaplicar2.html', context)
            questao.problema.get_usos()

    for algoritmo in avaliacao.algoritmos.all() :
        for idaluno in alunos :
            aluno=User.objects.get(id=idaluno)
            if not Aplicado.objects.filter(usuario=aluno,algoritmo=algoritmo).exists():
                aplicado,criado = Aplicado.objects.get_or_create(usuario=aluno,algoritmo=algoritmo)
                status,criado = AlgoritmoStatus.objects.get_or_create(aplicado=aplicado)
                for proposta in algoritmo.programa.propostas.all() :
                    codigo,criado = Codigo.objects.get_or_create(aplicado=aplicado,proposta=proposta)
            algoritmo.programa.get_usos()

class minhaThread (threading.Thread):
    def __init__(self, alunos, avaliacao):
        threading.Thread.__init__(self)
        self.alunos = alunos
        self.avaliacao = avaliacao
    def run(self):
        # print('run')
        aplicar(self.alunos, self.avaliacao)

@login_required
def avaliacaoaplicar2(request,id):
    avaliacao=Avaliacao.objects.get(id=id)
    if request.method == 'POST':
        idalunos = request.POST.getlist('alunos')
        # print(f'{idalunos} = {avaliacao}')
        thread1 = minhaThread(idalunos, avaliacao)
        thread1.start()

    return HttpResponseRedirect(reverse('professor:conhecimento'))



@login_required
def questaonovo(request,id):
    avaliacao=Avaliacao.objects.get(id=id)
    if request.method == 'POST':
        form=QuestaoForm(request.user,avaliacao,request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.avaliacao=avaliacao
            novo.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form=QuestaoForm(request.user,avaliacao)
    context = {'form':form,'id':id}
    return render(request, 'tarefa/questaonovo.html', context)

@login_required
def questaoeditar(request,id):
    questao=Questao.objects.get(id=id)
    avaliacao=questao.avaliacao
    if request.method == 'POST':
        form=QuestaoForm(request.user,avaliacao,request.POST,instance=questao)
        if form.is_valid():
            form.save()
            for aplicada in questao.aplicadas.all() :
                for status in aplicada.status.all() :
                    status.iniciou = None
                    status.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form = QuestaoForm(request.user,avaliacao,instance=questao)
    context = {'form':form,'id':questao.id}
    return render(request, 'tarefa/questaoeditar.html', context)


@login_required
def relatoriocorrigir1(request,id):
    questao=Questao.objects.get(id=id)
    aplicadas=questao.aplicadas.all()
    for aplicada in aplicadas :
        ## print("{}|{}".format(aplicada.id,aplicada.usuario))
        for relatorio in aplicada.relatorios_aplicada.all():
            ## print("{}|{}|{}".format(relatorio.id,relatorio.relatorio,relatorio.nota))
            relatorio.nota = 0
            relatorio.save()
    context = {'aplicadas':aplicadas}
    return render(request, 'tarefa/relatoriocorrigir1.html', context)

@login_required
def relatoriocorrigir2(request):
    if request.method == 'POST':
        corrigidos = request.POST.getlist('corrigidos')
        for corrigido in corrigidos :
            a=Relatorio.objects.get(id=corrigido)
            a.nota=1
            a.save()
    return HttpResponseRedirect(reverse('professor:conhecimento'))

@login_required
def anexocorrigir1(request,id):
    questao=Questao.objects.get(id=id)
    aplicadas=questao.aplicadas.all()
    for aplicada in aplicadas :
        ## print("{}|{}".format(aplicada.id,aplicada.usuario))
        for anexo in aplicada.anexos_aplicada.all():
            ## print("{}|{}|{}".format(anexo.id,anexo.anexo,anexo.nota))
            anexo.nota = 0
            anexo.save()
    context = {'aplicadas':aplicadas}
    return render(request, 'tarefa/anexocorrigir1.html', context)

@login_required
def anexocorrigir2(request):
    if request.method == 'POST':
        corrigidos = request.POST.getlist('corrigidos')
        for corrigido in corrigidos :
            a=Anexo.objects.get(id=corrigido)
            a.nota=1
            a.save()
    return HttpResponseRedirect(reverse('professor:conhecimento'))


@login_required
def aplicadaeditar(request,id):
    aplicada=Aplicada.objects.get(id=id)
    aplicada.ativo= not aplicada.ativo
    aplicada.save()
    context={}
    return render(request, 'tarefa/ok.html', context)


@login_required
def aplicadoeditar(request,id):
    aplicado=Aplicado.objects.get(id=id)
    aplicado.ativo= not aplicado.ativo
    aplicado.save()
    context={}
    return render(request, 'tarefa/ok.html', context)


@login_required
def relatorio(request,id):
    relatorio=Relatorio.objects.get(id=id)
    context = {'relatorio':relatorio}
    return render(request, 'tarefa/relatorio.html', context)



@login_required
def algoritmonovo(request,id):
    avaliacao=Avaliacao.objects.get(id=id)
    if request.method == 'POST':
        form=AlgoritmoForm(request.user,avaliacao,request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.avaliacao=avaliacao
            novo.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form=AlgoritmoForm(request.user,avaliacao)
    context = {'form':form,'id':id}
    return render(request, 'tarefa/algoritmonovo.html', context)

@login_required
def algoritmoeditar(request,id):
    algoritmo=Algoritmo.objects.get(id=id)
    avaliacao=algoritmo.avaliacao
    if request.method == 'POST':
        form=AlgoritmoForm(request.user,avaliacao,request.POST,instance=algoritmo)
        if form.is_valid():
            form.save()
            for aplicado in algoritmo.aplicados.all() :
                for status in aplicado.status_aplicado.all() :
                    status.iniciou = None
                    status.save()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form = AlgoritmoForm(request.user,avaliacao,instance=algoritmo)
    context = {'form':form,'id':algoritmo.id}
    return render(request, 'tarefa/algoritmoeditar.html', context)


@login_required
def codigo(request,id):
    codigo=Codigo.objects.get(id=id)
    context = {'codigo':codigo}
    return render(request, 'tarefa/codigo.html', context)



def execcmd(args, cwd = None, shell = False, kill_tree = True, timeout = -1, env = None):
    '''
    Run a command with a timeout after which it will be forcibly
    killed.
    '''
    p = Popen(args, shell = shell, cwd = cwd, stdout = PIPE, stderr = PIPE, env = env)
    try:
        stdout, stderr = p.communicate(timeout=timeout)
    except TimeoutExpired:
        pids = [p.pid]
        if kill_tree:
            pids.extend(get_process_children(p.pid))
        for pid in pids:
            try:
                kill(pid, SIGKILL)
            except OSError:
                pass
        return -9, '', ''
    return p.returncode, stdout, stderr

def get_process_children(pid):
    p = Popen('ps --no-headers -o pid --ppid %d' % pid, shell = True,
              stdout = PIPE, stderr = PIPE)
    stdout, stderr = p.communicate()
    return [int(p) for p in stdout.split()]


@login_required
def codigotestar(request,id):
    aplicado=Aplicado.objects.get(id=id)

    localmedia =  "{}/aplicado/".format(settings.MEDIA_ROOT)
    if not os.path.exists(localmedia):
        os.mkdir(localmedia)
    localmedia =  "{}/aplicado/{}/".format(settings.MEDIA_ROOT,aplicado.id)
    if not os.path.exists(localmedia):
        os.mkdir(localmedia)

    for codigo in aplicado.codigos_aplicado.all():
        arq = open("{}{}".format(localmedia,codigo.proposta.arquivo),encoding='utf-8', mode='w')
        if codigo.conteudo :
            arq.write(codigo.conteudo)
        else:
            arq.write('')
        arq.close()
    try:
        cmd='python {0}interface.py < {0}entrada.txt > {0}saida.txt'.format(localmedia)
        errorcode,sstdout,sstderr=execcmd(cmd, shell = True, timeout = 1)
    finally:
        pass

    saida=None
    if os.path.isfile(localmedia+'saida.txt'):
        arqsaida= open(localmedia+'saida.txt',encoding='utf-8', mode='r')
        saida=arqsaida.read()

    relatorio=None
    if os.path.isfile(localmedia+'relatorio.txt'):
        arqsaida= open(localmedia+'relatorio.txt',encoding='utf-8', mode='r')
        relatorio=arqsaida.read()

    output=sstderr.decode("utf-8")
    passou_testes=False
    tabela_testes=[]
    for teste in aplicado.algoritmo.programa.testes.all():
        if teste.entrada and teste.saida :
            arq = open("{0}{1}_entrada.txt".format(localmedia,teste.id,teste.entrada),encoding='utf-8', mode='w')
            arq.write(teste.entrada)
            arq.close()
            arq = open("{0}{1}_saida.txt".format(localmedia,teste.id,teste.saida),encoding='utf-8', mode='w')
            arq.write(teste.saida)
            arq.close()
            try:
                cmd='python {0}interface.py < {0}{1}_entrada.txt > {0}{1}_teste.txt'.format(localmedia,teste.id)
                execcmd(cmd, shell = True, timeout = 1)
            finally:
                pass
            arqsaida= open("{0}{1}_saida.txt".format(localmedia,teste.id),encoding='utf-8', mode='r')
            tsaida=arqsaida.read().strip()
            arqteste= open("{0}{1}_teste.txt".format(localmedia,teste.id),encoding='utf-8', mode='r')
            tteste=arqteste.read().strip()
            linha=[]
            linha.append(teste.id)
            linha.append(teste.entrada)
            linha.append(teste.saida)
            linha.append(tteste)
            if tsaida == tteste:
                passou_testes=True
                linha.append('Passou.')
                tabela_testes.append(linha)
            else:
                passou_testes=False
                linha.append('Não Passou.')
                tabela_testes.append(linha)
    context = {'aplicado':aplicado,'tabela_testes':tabela_testes}
    return render(request, 'tarefa/codigotestar.html', context)


@login_required
def codigocorrigir1(request,id):
    algoritmo=Algoritmo.objects.get(id=id)
    aplicados=algoritmo.aplicados.all()
    for aplicado in aplicados :
        ## print("{}|{}".format(aplicado.id,aplicado.usuario))
        for codigo in aplicado.codigos_aplicado.all():
            ## print("{}|{}|{}".format(codigo.id,codigo.codigo,codigo.nota))
            codigo.nota = 0
            codigo.save()
    context = {'aplicados':aplicados}
    return render(request, 'tarefa/codigocorrigir1.html', context)

@login_required
def codigocorrigir2(request):
    if request.method == 'POST':
        corrigidos = request.POST.getlist('corrigidos')
        for corrigido in corrigidos :
            a=Codigo.objects.get(id=corrigido)
            a.nota=1
            a.save()
    return HttpResponseRedirect(reverse('professor:conhecimento'))

@login_required
def valoresaleatoriosver(request,id):
    # print('oi')
    questao=Questao.objects.get(id=id)
    context = {'questao':questao}
    return render(request, 'tarefa/valoresaleatoriosver.html', context)

@login_required
def apagar(request,id):
    item = Avaliacao.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Questao.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Algoritmo.objects.filter(id=id)
    if item :
        item[0].delete()

    return HttpResponseRedirect(reverse('professor:conhecimento'))
