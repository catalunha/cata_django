from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date,timedelta,datetime,timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage


import os
from os import kill
#from subprocess import PIPE, Popen
from subprocess import call, Popen, PIPE, STDOUT, check_output,TimeoutExpired


from painel.models import User,Variavel
from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Teste
from tarefa.models import Avaliacao,Questao,Aplicada,Solucao,Relatorio,Anexo,Algoritmo,Aplicado,Codigo
from professor.models import QuestaoStatus,AlgoritmoStatus
from instituicao.models import Instituicao,Conhecimento,Turma
from aluno.forms import CodigoForm

@login_required
def atuais(request):
    # # print('+++ aluno->views.py->atuais +++')
    hojeagora=datetime.now()
    # # print('hojeagora:{}'.format(hojeagora))
    usuario = request.user
    # # print('usuario:{}'.format(usuario))
    turmas=usuario.na_turma.all()
    turmas=turmas.filter(ativo=True)
    # # print('turmas:{}'.format(turmas))
    avaliacoes=Avaliacao.objects.filter(turma__in=turmas,ativo=True,inicio__lte=hojeagora,fim__gte=hojeagora)
    # # print('avaliacoes:{}'.format(avaliacoes))
    questoes=Questao.objects.filter(avaliacao__in=avaliacoes,ativo=True,problema__ativo=True)
    # # print('questoes:{}'.format(questoes))
    aplicadas=Aplicada.objects.filter(usuario=usuario,questao__in=questoes,ativo=True)
    # # print('aplicadas:{}'.format(aplicadas))

    algoritmos=Algoritmo.objects.filter(avaliacao__in=avaliacoes,ativo=True,programa__ativo=True)
    # # print('algoritmos:{}'.format(algoritmos))
    aplicados=Aplicado.objects.filter(usuario=usuario,algoritmo__in=algoritmos,ativo=True)
    # # print('aplicados:{}'.format(aplicados))


    questaostatus=QuestaoStatus.objects.filter(aplicada__in=aplicadas)
    for status in questaostatus:
        status.save()
    # print('questaostatus:{}'.format(questaostatus))

    algoritmostatus=AlgoritmoStatus.objects.filter(aplicado__in=aplicados)
    for status in algoritmostatus:
        status.save()
    # print('algoritmostatus:{}'.format(algoritmostatus))

    # print('--- aluno->views.py->atuais ---')
    context = {'turmas':turmas,'avaliacoes':avaliacoes,'aplicadas':aplicadas,'aplicados':aplicados}
    return render(request, 'aluno/atuais.html', context)



def is_number(s):
    try:
        valor=float(s)
        return True, valor
    except ValueError:
        pass

    try:
        import unicodedata
        valor=float(unicodedata.numeric(s))
        return True,valor
    except (TypeError, ValueError):
        pass

    return False,s

@login_required
def editar(request,id):
    aplicada=Aplicada.objects.get(id=id)
    status=QuestaoStatus.objects.get(aplicada=aplicada)
    if status.iniciou is None :
        status.iniciou=datetime.now(timezone.utc)
    status.save()
    if not status.ativo:
        return HttpResponseRedirect(reverse('aluno:atuais'))

    if request.method == 'POST':
        for solucao in aplicada.solucoes_aplicada.all():
            resposta = request.POST.get('resposta_'+solucao.resposta.letra)
            ## print("Resposta da letra {}={}".format(solucao.resposta.letra,resposta))
            if resposta:
                solucao.solucao=resposta
                solucao.save()

        for anexo in aplicada.anexos_aplicada.all():
            arq=request.FILES.get('anexo_'+anexo.arquivo.letra)
            ## print("Arquivo da letra {}={}".format(anexo.arquivo.letra,arq))
            if arq:
                pasta = '/tarefa/anexo/anexo'
                fs = FileSystemStorage(location='{}{}'.format(settings.MEDIA_ROOT,pasta))
                novonome ='{}_{}'.format(id,arq.name)
                filename = fs.save(novonome, arq)
                anexo.anexo.name='{}/{}'.format(pasta,novonome)
                anexo.save()

        for relatorio in aplicada.relatorios_aplicada.all():
            texto = request.POST.get('texto_'+relatorio.texto.letra)
            ## print("Relatório da letra {}={}".format(relatorio.texto.letra,texto))
            if texto:
                relatorio.relatorio=texto
                relatorio.save()

        status.tentou()


        variavel = Variavel.objects.get(usuario=aplicada.questao.avaliacao.turma.conhecimento.usuario,nome='nota_variacao')
        try:
            a,nota_variacao=is_number(variavel.valor)
            nota_variacao=nota_variacao/100.0
            nota_variacao_min=(1-nota_variacao)
            nota_variacao_max=(1+nota_variacao)
        except:
            print("Erro na conversao da nota_variacao para {}".format(nota_variacao.usuario.last_name))

        for solucao in aplicada.solucoes_aplicada.all():
            # print("{}:{}={}".format(solucao.resposta.letra,solucao.solucao,solucao.resposta.valor))
            if solucao.solucao:
                solucao.nota = None
                ehnumeroGab,vlrGab = is_number(solucao.resposta.valor)
                ehnumeroAluno,vlrAluno = is_number(solucao.solucao)
                if ehnumeroGab and ehnumeroAluno :
                    try:
                        if vlrGab > 0 :
                            if vlrGab*nota_variacao_min <= vlrAluno <= vlrGab*nota_variacao_max :
                                solucao.nota = 1
                        else:
                            if vlrGab*nota_variacao_min >= vlrAluno >= vlrGab*nota_variacao_max :
                                solucao.nota = 1
                    except:
                        solucao.nota = None
                        print("Erro na conversao de valores para nota em view.py")
                else:
                    if vlrGab==vlrAluno:
                        solucao.nota = 1
                solucao.save()

    variaveisAleatorias=None
    solucoes=Solucao.objects.filter(aplicada=aplicada)
    if solucoes:
        solucao=solucoes[0]
        variaveisAleatorias=solucao.resposta.simulacao.valores_aleatorios.all()
    anexos=Anexo.objects.filter(aplicada=aplicada)
    if anexos:
        anexo=anexos[0]
        variaveisAleatorias=anexo.arquivo.simulacao.valores_aleatorios.all()
    relatorios=Relatorio.objects.filter(aplicada=aplicada)
    if relatorios:
        relatorio=relatorios[0]
        variaveisAleatorias=relatorio.texto.simulacao.valores_aleatorios.all()

    context = {'aplicada':aplicada,'status':status,'variaveisAleatorias':variaveisAleatorias}
    return render(request, 'aluno/editar.html', context)


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
                import signal
                kill(pid, signal.SIGKILL)
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
def editaralgoritmo(request,id):
    aplicado=Aplicado.objects.get(id=id)
    status=AlgoritmoStatus.objects.get(aplicado=aplicado)
    if status.iniciou is None :
        status.iniciou=datetime.now(timezone.utc)
    status.save()
    if not status.ativo:
        return HttpResponseRedirect(reverse('aluno:atuais'))

    try:
        cmd="ps axf | grep interface.dart | grep -v grep | awk '{print \"kill -9 \" $1}' | sh"
        execcmd(cmd, shell = True, timeout = 1)
    finally:
        pass

    if request.method == 'POST':
        for codigo in aplicado.codigos_aplicado.all():
            valor = request.POST.get('entrada')
            if codigo.proposta.arquivo == 'entrada.txt':
                codigo.conteudo=valor
            valor = request.POST.get('interface')
            if codigo.proposta.arquivo == 'interface.dart':
                codigo.conteudo=valor
            valor = request.POST.get('solucao')
            if codigo.proposta.arquivo == 'solucao.dart':
                codigo.conteudo=valor
            valor = request.POST.get('dados')
            if codigo.proposta.arquivo == 'dados.txt':
                codigo.conteudo=valor
            codigo.save()

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
            cmd='dart {0}interface.dart < {0}entrada.txt > {0}saida.txt'.format(localmedia)
            errorcode,sstdout,sstderr=execcmd(cmd, shell = True, timeout = 1)
        finally:
            pass


        saida=""
        if os.path.isfile(localmedia+'saida.txt'):
            arqsaida= open(localmedia+'saida.txt',encoding='utf-8', mode='r')
            saida=arqsaida.read()

        relatorio=""
        if os.path.isfile(localmedia+'relatorio.txt'):
            arqsaida= open(localmedia+'relatorio.txt',encoding='utf-8', mode='r')
            relatorio=arqsaida.read()

        output=sstderr.decode("utf-8")
        passou_testes=False
        for teste in aplicado.algoritmo.programa.testes.all():
            if teste.entrada and teste.saida :
                arq = open("{0}{1}_entrada.txt".format(localmedia,teste.id,teste.entrada),encoding='utf-8', mode='w')
                arq.write(teste.entrada)
                arq.close()
                arq = open("{0}{1}_saida.txt".format(localmedia,teste.id,teste.saida),encoding='utf-8', mode='w')
                arq.write(teste.saida)
                arq.close()
                try:
                    cmd='dart {0}interface.dart < {0}{1}_entrada.txt > {0}{1}_teste.txt'.format(localmedia,teste.id)
                    execcmd(cmd, shell = True, timeout = 1)
                finally:
                    pass
                arqsaida= open("{0}{1}_saida.txt".format(localmedia,teste.id),encoding='utf-8', mode='r')
                tsaida=arqsaida.read().strip()
                arqteste= open("{0}{1}_teste.txt".format(localmedia,teste.id),encoding='utf-8', mode='r')
                tteste=arqteste.read().strip()
                if tsaida == tteste:
                    passou_testes=True
                else:
                    passou_testes=False
                    break
        for codigo in aplicado.codigos_aplicado.all():
            if passou_testes :
                codigo.nota=1
            else:
                codigo.nota=0
            codigo.save()
        context = {'aplicado':aplicado,'status':status,'saida':saida,'relatorio':relatorio,'output':output,'passou_testes':passou_testes}
        return render(request, 'aluno/editaralgoritmo.html', context)


    codigos = aplicado.codigos_aplicado.all()
    saida=None
    relatorio=None
    output=None
    passou_testes=None

    context = {'aplicado':aplicado,'status':status,'saida':saida,'relatorio':relatorio,'output':output,'passou_testes':passou_testes}
    return render(request, 'aluno/editaralgoritmo.html', context)


@login_required
def todas(request):
    hojeagora=datetime.now()
    usuario = request.user
    turmas=usuario.na_turma.all()
    turmas=turmas.filter(ativo=True)
    avaliacoes=Avaliacao.objects.filter(turma__in=turmas,ativo=True,inicio__lte=hojeagora)

    questoes=Questao.objects.filter(avaliacao__in=avaliacoes,ativo=True,problema__ativo=True)
    aplicadas=Aplicada.objects.filter(usuario=usuario,questao__in=questoes,ativo=True)

    algoritmos=Algoritmo.objects.filter(avaliacao__in=avaliacoes,ativo=True,programa__ativo=True)
    aplicados=Aplicado.objects.filter(usuario=usuario,algoritmo__in=algoritmos,ativo=True)


    questaostatus=QuestaoStatus.objects.filter(aplicada__in=aplicadas)
    for status in questaostatus:
        status.save()

    algoritmostatus=AlgoritmoStatus.objects.filter(aplicado__in=aplicados)
    for status in algoritmostatus:
        status.save()

    context = {'turmas':turmas,'avaliacoes':avaliacoes,'aplicadas':aplicadas,'aplicados':aplicados}
    return render(request, 'aluno/todas.html', context)

@login_required
def publica(request):
    usuario = request.user
    turmas=usuario.na_turma.all()
    avaliacoes=Avaliacao.objects.filter(privada=False,turma__in=turmas,ativo=True)

    questoes=Questao.objects.filter(avaliacao__in=avaliacoes,ativo=True,problema__ativo=True)
    aplicadas=Aplicada.objects.filter(questao__in=questoes,ativo=True)


    algoritmos=Algoritmo.objects.filter(avaliacao__in=avaliacoes,ativo=True,programa__ativo=True)
    aplicados=Aplicado.objects.filter(algoritmo__in=algoritmos,ativo=True)

    context = {'aplicadas':aplicadas,'aplicados':aplicados}
    return render(request, 'aluno/publica.html', context)
