from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from datetime import date,timedelta,datetime,timezone

from situacao.models import Indice,Problema,Simulacao,ValorAleatorio,Resposta,Arquivo,Texto,Programa,Teste,Proposta
from situacao.forms import IndiceForm,Indice2Form,ProblemaForm,Problema2Form,ValorAleatorioForm,RespostaForm,TextoForm,ArquivoForm,ProgramaForm,Programa2Form,PropostaForm,TesteForm
from tarefa.models import Questao
'''
@login_required
def indicenovo(request):
    if request.method == 'POST':
        form=IndiceForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form=IndiceForm(request.user)
    context = {'form':form}
    return render(request, 'situacao/indicenovo.html', context)
'''
@login_required
def indiceeditar(request,id):
    indice=Indice.objects.get(id=id)
    if request.method == 'POST':
        form=Indice2Form(request.POST,instance=indice)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form = Indice2Form(instance=indice)
    context = {'form':form,'indice':indice}
    return render(request, 'situacao/indiceeditar.html', context)


@login_required
def indiceitem(request,id):
    indice=Indice.objects.get(id=id)
    if request.method == 'POST':
        form=IndiceForm(request.POST)
        if form.is_valid():
            #form.save()
            novo=form.save(commit=False)
            novo.superior=indice.superior
            novo.conhecimento=indice.conhecimento
            novo.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        #form = IndiceForm(initial={'superior': indice.superior,'conhecimento':indice.conhecimento})
        form = IndiceForm()
    context = {'form':form,'indice':indice}
    return render(request, 'situacao/indiceitem.html', context)

@login_required
def indicesubitem(request,id):
    indice=Indice.objects.get(id=id)
    if request.method == 'POST':
        form=IndiceForm(request.POST)
        if form.is_valid():
            #form.save()
            novo=form.save(commit=False)
            novo.superior=indice
            novo.conhecimento=indice.conhecimento
            novo.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        #form = IndiceForm(initial={'superior': indice,'conhecimento':indice.conhecimento})
        form = IndiceForm()
    context = {'form':form,'indice':indice}
    return render(request, 'situacao/indicesubitem.html', context)


@login_required
def sobe(request,id):
    indice=Indice.objects.get(id=id)
    indice.subir_ordem()
    return HttpResponseRedirect(reverse('professor:indice'))

@login_required
def desce(request,id):
    indice=Indice.objects.get(id=id)
    indice.descer_ordem()
    return HttpResponseRedirect(reverse('professor:indice'))


@login_required
def problemanovo(request,id):
    indice=Indice.objects.get(id=id)
    if request.method == 'POST':
        form=ProblemaForm(request.POST,request.FILES)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.usuario=request.user
            novo.save()
            novo.indices.add(indice)
            form.save_m2m()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form=ProblemaForm()
    context = {'form':form,'indice':indice}
    return render(request, 'situacao/problemanovo.html', context)

@login_required
def problemaeditar(request,id):
    problema=Problema.objects.get(id=id)
    if request.method == 'POST':
        form=Problema2Form(request.POST,request.FILES,instance=problema)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form = Problema2Form(instance=problema)
    context = {'form':form,'id':problema.id}
    return render(request, 'situacao/problemaeditar.html', context)

@login_required
def texto(request,id):
    texto=Texto.objects.get(id=id)
    context = {'texto':texto}
    return render(request, 'situacao/texto.html', context)

@login_required
def simulacao(request,id):
    usuario = request.user
    problema=Problema.objects.get(id=id,ativo=True)
    context = {'problema':problema}
    return render(request, 'situacao/simulacao.html', context)


@login_required
def simulacaonovo(request,id):
    problema=Problema.objects.get(id=id)
    Simulacao(problema=problema).save()
    return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': id}))

@login_required
def simulacaoapagar(request,id):
    simulacao=Simulacao.objects.get(id=id)
    Questao.objects.filter(problema=simulacao.problema).delete()
    simulacao.delete()
    return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': simulacao.problema.id}))


@login_required
def simulacaoapagartodas(request,id):
    Questao.objects.filter(problema__id=id).delete()
    Simulacao.objects.filter(problema__id=id).delete()
    return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': id}))



@login_required
def simulacaoimportar(request,id):
    if request.method == 'POST':
        simulacoes = request.POST.get('simulacoes')
        ## print(simulacoes)
        linhas=simulacoes.split('\n')
        for linha in linhas :
            if linha.strip() :
                ## print(linha)
                problema=Problema.objects.get(id=id)
                sim=Simulacao(problema=problema)
                sim.save()
                listadalinha=linha.strip().split('|')
                VA=listadalinha[0]
                if VA :
                    ## print('VA')
                    NVA=VA.strip().split(',')
                    for nva in NVA :
                        valor=nva.strip().split('=')
                        ## print("{}:{}".format(valor[0],valor[1]))
                        tbVA=ValorAleatorio(simulacao=sim,nome=valor[0],valor=valor[1]).save()

                R=listadalinha[1]
                if R :
                    ## print('R')
                    LR=R.strip().split(',')
                    for item in LR :
                        valor=item.strip().split('=')
                        ## print("{}:{}".format(valor[0],valor[1]))
                        tbR=Resposta(simulacao=sim,letra=valor[0],valor=valor[1]).save()

                A=listadalinha[2]
                if A :
                    ## print('A')
                    LA=A.strip().split(',')
                    for letra in LA :
                        ## print("{}".format(letra))
                        tbA=Arquivo(simulacao=sim,letra = letra).save()

                T=listadalinha[3]
                if T :
                    ## print('T')
                    LT=T.strip().split(',')
                    for letra in LT :
                        ## print("{}".format(letra))
                        tbT=Texto(simulacao=sim,letra = letra).save()

        return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': id}))
    context = {'id':id}
    return render(request, 'situacao/simulacaoimportar.html', context)

@login_required
def vlraleatnovo(request,id):
    if request.method == 'POST':
        form=ValorAleatorioForm(request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            simulacao=Simulacao.objects.get(id=id)
            novo.simulacao=simulacao
            novo.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': simulacao.problema.id}))
    else:
        form=ValorAleatorioForm()
    context = {'form':form,'id':id}
    return render(request, 'situacao/vlraleatnovo.html', context)

@login_required
def vlraleateditar(request,id):
    va=ValorAleatorio.objects.get(id=id)
    if request.method == 'POST':
        form=ValorAleatorioForm(request.POST,instance=va)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': va.simulacao.problema.id}))
    else:
        form = ValorAleatorioForm(instance=va)
    context = {'form':form,'id':id}
    return render(request, 'situacao/vlraleateditar.html', context)


@login_required
def respostanovo(request,id):
    if request.method == 'POST':
        form=RespostaForm(request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            simulacao=Simulacao.objects.get(id=id)
            novo.simulacao=simulacao
            novo.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': simulacao.problema.id}))
    else:
        form=RespostaForm()
    context = {'form':form,'id':id}
    return render(request, 'situacao/respostanovo.html', context)

@login_required
def respostaeditar(request,id):
    resposta=Resposta.objects.get(id=id)
    if request.method == 'POST':
        form=RespostaForm(request.POST,instance=resposta)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': resposta.simulacao.problema.id}))
    else:
        form = RespostaForm(instance=resposta)
    context = {'form':form,'id':id}
    return render(request, 'situacao/respostaeditar.html', context)


@login_required
def textonovo(request,id):
    if request.method == 'POST':
        form=TextoForm(request.POST)
        if form.is_valid():
            novo=form.save(commit=False)
            simulacao=Simulacao.objects.get(id=id)
            novo.simulacao=simulacao
            novo.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': simulacao.problema.id}))
    else:
        form=TextoForm()
    context = {'form':form,'id':id}
    return render(request, 'situacao/textonovo.html', context)

@login_required
def textoeditar(request,id):
    texto=Texto.objects.get(id=id)
    if request.method == 'POST':
        form=TextoForm(request.POST,instance=texto)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': texto.simulacao.problema.id}))
    else:
        form = TextoForm(instance=texto)
    context = {'form':form,'id':id}
    return render(request, 'situacao/textoeditar.html', context)

@login_required
def anexonovo(request,id):
    if request.method == 'POST':
        form=ArquivoForm(request.POST,request.FILES,)
        if form.is_valid():
            novo=form.save(commit=False)
            simulacao=Simulacao.objects.get(id=id)
            novo.simulacao=simulacao
            novo.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': simulacao.problema.id}))
    else:
        form=ArquivoForm()
    context = {'form':form,'id':id}
    return render(request, 'situacao/anexonovo.html', context)

@login_required
def anexoeditar(request,id):
    arquivo=Arquivo.objects.get(id=id)
    if request.method == 'POST':
        form=ArquivoForm(request.POST,request.FILES,instance=arquivo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('situacao:simulacao',kwargs={'id': arquivo.simulacao.problema.id}))
    else:
        form = ArquivoForm(instance=arquivo)
    context = {'form':form,'id':id}
    return render(request, 'situacao/anexoeditar.html', context)


@login_required
def programanovo(request,id):
    indice=Indice.objects.get(id=id)
    if request.method == 'POST':
        form=ProgramaForm(request.POST,request.FILES)
        if form.is_valid():
            novo=form.save(commit=False)
            novo.usuario=request.user
            novo.save()
            novo.indices.add(indice)
            form.save_m2m()
            proposta,criado = Proposta.objects.get_or_create(programa=novo,arquivo='interface.dart')
            proposta,criado = Proposta.objects.get_or_create(programa=novo,arquivo='solucao.dart')
            proposta,criado = Proposta.objects.get_or_create(programa=novo,arquivo='entrada.txt')
            proposta,criado = Proposta.objects.get_or_create(programa=novo,arquivo='dados.txt')
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form=ProgramaForm()
    context = {'form':form,'indice':indice}
    return render(request, 'situacao/programanovo.html', context)


@login_required
def programaeditar(request,id):
    programa=Programa.objects.get(id=id)
    if request.method == 'POST':
        form=Programa2Form(request.POST,request.FILES,instance=programa)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form = Programa2Form(instance=programa)
    context = {'form':form,'id':programa.id}
    return render(request, 'situacao/programaeditar.html', context)


@login_required
def propostaeditar(request,id):
    proposta=Proposta.objects.get(id=id)
    if request.method == 'POST':
        form=PropostaForm(request.POST,instance=proposta)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form = PropostaForm(instance=proposta)
    context = {'form':form,'proposta':proposta}
    return render(request, 'situacao/propostaeditar.html', context)


@login_required
def proposta(request,id):
    proposta=Proposta.objects.get(id=id)
    context = {'proposta':proposta}
    return render(request, 'situacao/proposta.html', context)


@login_required
def testenovo(request,id):
    programa=Programa.objects.get(id=id)
    Teste(programa=programa).save()
    return HttpResponseRedirect(reverse('professor:indice'))



@login_required
def testeeditar(request,id):
    teste=Teste.objects.get(id=id)
    if request.method == 'POST':
        form=TesteForm(request.POST,instance=teste)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('professor:indice'))
    else:
        form = TesteForm(instance=teste)
    context = {'form':form,'id':id}
    return render(request, 'situacao/testeeditar.html', context)



@login_required
def apagar(request,id):
    item = Indice.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Problema.objects.filter(id=id)
    if item :
        item[0].delete()
    item = ValorAleatorio.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Resposta.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Texto.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Arquivo.objects.filter(id=id)
    if item :
        item[0].delete()
    item = Teste.objects.filter(id=id)
    if item :
        item[0].delete()

    return HttpResponseRedirect(reverse('professor:indice'))
