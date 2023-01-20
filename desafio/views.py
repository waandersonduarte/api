from django.shortcuts import render, redirect
from desafio.models import Upload, DadosArquivo
from desafio.forms import UploadForm
from desafio.serializers import *
from django.contrib import messages
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
import sqlite3
from datetime import date



def index(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            carregar_arquivo(request.FILES['arquivo'])
            arquivo = form.save(commit=False)
            messages.success(request, 'Arquivo enviado com sucesso!')
            arquivo.save()
            return redirect('index')
    else:
        form = UploadForm()
        return render(request, 'desafio/upload.html', {'form': form})

def carregar_arquivo(dado):
    with open('uploads/arquivo.xlsx', 'wb+') as arquivo:
        for chunk in dado.chunks():
            arquivo.write(chunk)
        arquivo.close()

    arquivo = pd.read_excel('uploads/arquivo.xlsx')
    for i, DADOS in enumerate(arquivo['id']):
        id = arquivo.loc[i, 'id']
        nome = arquivo.loc[i, 'nome']
        sobrenome = arquivo.loc[i, 'sobrenome']
        sexo = arquivo.loc[i, 'sexo']
        altura = arquivo.loc[i, 'altura']
        peso = arquivo.loc[i, 'peso']
        dt_nascimento = str(arquivo.loc[i, 'nascimento'])
        bairro = arquivo.loc[i, 'bairro']
        cidade = arquivo.loc[i, 'cidade']
        estado = arquivo.loc[i, 'estado']
        numero = arquivo.loc[i, 'numero']
        
        dia = int(dt_nascimento[0])
        mes = int(dt_nascimento[1])
        ano = int(dt_nascimento[2:6])

        if mes == 0:
            mes = int(dt_nascimento[5])
        nascimento = date(day=dia, month=mes, year=ano).strftime('%d/%m/%Y')
        
        conectar = sqlite3.connect('db.sqlite3')
        dados = '('+'\''+str(id)+'\''+', \''+str(nome)+'\''+', \''+str(sobrenome)+'\''+', \
                \''+str(sexo)+'\''+', \''+str(altura)+'\''+', \''+str(peso)+'\''+', \
                \''+str(nascimento)+'\''+', \''+str(bairro)+'\''+', \''+str(cidade)+'\''+', \
                \''+str(estado)+'\''+', \''+str(numero)+'\''+')'
        comando = 'INSERT INTO desafio_dadosarquivo (id, nome, sobrenome, \
                    sexo, altura, peso, nascimento, bairro, cidade, estado, numero) VALUES'
        sql = comando + dados
        
        try:
            cursor = conectar.cursor()
            cursor.execute(sql)
            conectar.commit()
        except:
            continue
        
    conectar.close()
   
class MulheresDeMereenViewSet(viewsets.ModelViewSet):
    queryset = DadosArquivo.objects.filter(sexo__contains='F', cidade__contains='Meeren')
    serializer_class = MulheresDeMereenSerializer
    
    
class ListaDePessoasViewSet(viewsets.ModelViewSet):
    queryset = DadosArquivo.objects.all()
    serializer_class = ListaDePessoasSerializer
    #TODO: README
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['nome', 'sobrenome']
    ordering_fields = ['nascimento']
    filterset_fields = ['sexo']
    