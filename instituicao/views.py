from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date,timedelta,datetime,timezone
import os
from django.conf import settings
import threading


from instituicao.models import Conhecimento,Turma
from instituicao.forms import ConhecimentoForm,TurmaForm
from professor.models import Ementa

from painel.models import Variavel
from situacao.models import Indice,Problema,Programa


@login_required
def conhecimentonovo(request):
    if request.method == 'POST':
        form=ConhecimentoForm(request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.usuario=request.user
            novo.save()
            indice,criado = Indice.objects.get_or_create(conhecimento=novo,nome=novo.nome,superior=None)
            indice.save()
            ementa,criado = Ementa.objects.get_or_create(conhecimento=novo)
            ementa.texto='# Seja bem vindo.'
            ementa.save()
            var,criado = Variavel.objects.get_or_create(usuario=request.user,nome='nota_variacao')
            var.valor = '10'
            var.save()
            return HttpResponseRedirect(reverse('professor:acoes'))
    else:
        form=ConhecimentoForm()
    context = {'form':form}
    return render(request, 'instituicao/conhecimentonovo.html', context)


@login_required
def conhecimentoeditar(request,id):
    conhecimento=Conhecimento.objects.get(id=id)
    if request.method == 'POST':
        form=ConhecimentoForm(request.POST,instance=conhecimento)
        if form.is_valid():
            form.save()
            if not conhecimento.ativo :
                turmas=conhecimento.turmas.all()
                for turma in turmas :
                    turma.ativo=False
                    turma.save()
                problemas=Problema.objects.filter(usuario=request.user,ativo=True)
                for problema in problemas:
                    problema.get_usos()
                programas=Programa.objects.filter(usuario=request.user,ativo=True)
                for programa in programas:
                    programa.get_usos()

            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
         form = ConhecimentoForm(instance=conhecimento)
    context = {'form':form,'id':conhecimento.id,'tempo':conhecimento}
    return render(request, 'instituicao/conhecimentoeditar.html', context)


@login_required
def turmanovo(request,id):
    conhecimento=Conhecimento.objects.get(id=id)
    if request.method == 'POST':
        form=TurmaForm(request.POST)
        if form.is_valid():
            #form.save()
            novo=form.save(commit=False)
            novo.conhecimento=conhecimento
            novo.save()

            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form=TurmaForm()
    context = {'form':form,'conhecimento':conhecimento}
    return render(request, 'instituicao/turmanovo.html', context)

@login_required
def turmaeditar(request,id):
    turma=Turma.objects.get(id=id)
    if request.method == 'POST':
        form=TurmaForm(request.POST,instance=turma)
        if form.is_valid():
            form.save()
            problemas=Problema.objects.filter(usuario=request.user,ativo=True)
            for problema in problemas:
                problema.get_usos()
            programas=Programa.objects.filter(usuario=request.user,ativo=True)
            for programa in programas:
                programa.get_usos()
            return HttpResponseRedirect(reverse('professor:conhecimento'))
    else:
        form = TurmaForm(instance=turma)
    context = {'form':form,'id':turma.id,'tempo':turma}
    return render(request, 'instituicao/turmaeditar.html', context)



def atualizarnotas(turma):
    # usuario = request.user
    # turma=Turma.objects.get(id=id)
    arqnome = turma.nome.replace(' ','-')+'.csv'
    notas2=[]
    arq = os.path.join(settings.MEDIA_ROOT,arqnome)
    arqw = open(arq,'w')
    arqw.write("conhecimento;turma;aluno.nome;aluno.numero;avaliacao.nome;avaliacao.nota;questao.numero;questao.referencia;questao.descricao;questao.nota;solucao;anexo;relatorio;solucao.letra;anexo.letra;relatorio.letra;\n")
    for aluno in turma.alunos.all():
        for aplicada in aluno.aplicadas_usuario.all():
            linha=[]
            if aplicada.ativo and aplicada.questao.ativo and aplicada.questao.problema.ativo and aplicada.questao.avaliacao.ativo and aplicada.questao.avaliacao.turma.id == turma.id:
                #linha.append(turma.conhecimento.instituicao.nome)
                #linha.append(turma.conhecimento.usuario.last_name)
                linha.append(turma.conhecimento.nome)
                linha.append(turma.nome)
                linha.append(aluno.last_name)
                linha.append(aluno.username)
                linha.append(aplicada.questao.avaliacao.nome)
                linha.append(aplicada.questao.avaliacao.nota)
                linha.append(aplicada.questao.numero)
                #linha.append(aplicada.questao.id)
                linha.append(aplicada.questao.problema.referencia)
                linha.append(aplicada.questao.problema.descricao)
                linha.append(aplicada.questao.nota)
                linha.append(aplicada.get_total_solucao())
                linha.append(aplicada.get_total_anexo())
                linha.append(aplicada.get_total_relatorio())
                a='='
                for solucao in aplicada.solucoes_aplicada.all():
                    a = a + '+{}'.format(solucao.nota)
                linha.append(a)
                a='='
                for anexo in aplicada.anexos_aplicada.all():
                    a = a + '+{}'.format(anexo.nota)
                linha.append(a)
                a='='
                for relatorio in aplicada.relatorios_aplicada.all():
                    a = a + '+{}'.format(relatorio.nota)
                linha.append(a)
                ## print(';'.join(map(str, linha)))
                #notas2.append(linha)
                arqw.write(';'.join(map(str, linha)))
                arqw.write("\n")
        for aplicado in aluno.aplicados_usuario.all():
            linha=[]
            if aplicado.ativo and aplicado.algoritmo.ativo and aplicado.algoritmo.programa.ativo and aplicado.algoritmo.avaliacao.ativo and aplicado.algoritmo.avaliacao.turma.id == turma.id:
                #linha.append(turma.conhecimento.instituicao.nome)
                #linha.append(turma.conhecimento.usuario.last_name)
                linha.append(turma.conhecimento.nome)
                linha.append(turma.nome)
                linha.append(aluno.last_name)
                linha.append(aluno.username)
                linha.append(aplicado.algoritmo.avaliacao.nome)
                linha.append(aplicado.algoritmo.avaliacao.nota)
                linha.append(aplicado.algoritmo.numero)
                #linha.append(aplicado.algoritmo.id)
                linha.append(aplicado.algoritmo.programa.referencia)
                linha.append(aplicado.algoritmo.programa.descricao)
                linha.append(aplicado.algoritmo.nota)
                linha.append(aplicado.get_total_codigo())
                linha.append("")
                linha.append("")
                a='='
                for codigo in aplicado.codigos_aplicado.all():
                    a = a + '+{}'.format(codigo.nota)
                linha.append(a)
                linha.append("")
                linha.append("")
                #notas2.append(linha)
                arqw.write(';'.join(map(str, linha)))
                arqw.write("\n")
    '''
    for nota in notas2:
        for linha in nota:
            arqw.write('{};'.format(linha))
        arqw.write("\n")
    '''
    arqw.close()


class minhaThread (threading.Thread):
    def __init__(self, turma):
        threading.Thread.__init__(self)
        self.turma = turma
    def run(self):
        # print('run')
        atualizarnotas(self.turma)


@login_required
def notas(request,id):

    usuario = request.user
    turma=Turma.objects.get(id=id)
    arqnome = turma.nome.replace(' ','-')+'.csv'

    thread1 = minhaThread(turma)
    thread1.start()
   
    context = {'arq':arqnome}
    return render(request, 'instituicao/notas.html', context)




@login_required
def apagar(request,id):
    item = Conhecimento.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Turma.objects.filter(id=id)
    if item :
        item[0].delete()

    return HttpResponseRedirect(reverse('professor:conhecimento'))
