# API - Django Rest Framework
O foco do projeto é o desenvolvimento de uma API para consumir os dados de um arquivo excel.
O Django Rest Framework auxilia na usabilidade do sistema facilitando a manipulação das informações contidas no Banco de Dados. Além disso, contém sistema de autenticação e serialização dos dados.

## Criando o diretório do projeto
```
mkdir desafio_api
cd clinica_api
```

## Criando o ambiente virtual
```
virtualenv venv
. venv/bin/activate  
```

## Instalando as ferramentas necessárias para nossa aplicação
```
pip install django
pip install djangorestframework
pip install markdown       
pip install django-filter
pip install pandas
pip install openpyxl
```

## Criando o projeto e a aplicação
```
django-admin startproject core .  
django-admin startapp desafio
```

## Configurando o settings.py
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'desafio',
]
```

## Criando os modelos para o nosso desafio de consumir um arquivo 
No arquivo ``desafio/models.py`` definimos todos os objetos chamados Modelos, este é um lugar em que vamos definir os relacionamentos entre as classes que estaram presentes na nossa clinica definidos no nosso diagrama e classes.

Vamos abrir ``desafio/models.py`` no editor de código, apagar tudo dele e escrever o seguinte código:

```python
from django.db import models

class Upload(models.Model):
    arquivo = models.FileField()

class DadosArquivo(models.Model):
    SEXO = (
    ('M', 'Masculino'),
    ('F', 'Feminino'))

    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50, blank=False, verbose_name='Nome:')
    sobrenome = models.CharField(max_length=50, blank=False, verbose_name='Sobrenome:')
    sexo = models.CharField(max_length=1, choices=SEXO, null=False, default='M', verbose_name='Gênero:')
    altura = models.FloatField(verbose_name='Altura:')
    peso = models.FloatField(verbose_name='Peso:')
    nascimento = models.CharField(max_length=50, verbose_name='Data de Nascimento:')
    bairro = models.CharField(max_length=50, verbose_name='Bairro:')
    cidade = models.CharField(max_length=50, verbose_name='Cidade:')
    estado = models.CharField(max_length=50, verbose_name='Estado:')
    numero = models.PositiveIntegerField(verbose_name='Número:')
    
   
    def __str__(self):
        return self.nome
```

Preparar e migrar nossos modelos para a base de dados:
```
python manage.py makemigrations
python manage.py migrate
```

## Admin
```
python manage.py createsuperuser
```
Vamos abrir o arquivo ``desafio/admin.py``, apagar tudo e acrescentar o seguinte código:
```python
from django.contrib import admin
from desafio.models import *

class DadosArquivoExcel(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)
    list_filter = ('nome',)
    
    list_per_page = 10
    ordering = ('nascimento',)

admin.site.register(DadosArquivo, DadosArquivoExcel)

class Uploads(admin.ModelAdmin):
    list_display = ('id', 'arquivo')
    list_display_links = ('id', 'arquivo')
    search_fields = ('arquivo',)
    list_filter = ('arquivo',)

admin.site.register(Upload, Uploads)
```

## Serializers
Iremos criar um arquivo ``desafio/serializers.py``:

```python
from rest_framework import serializers
from desafio.models import *

class MulheresDeMereenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosArquivo
        fields = '__all__'
        

class ListaDePessoasSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosArquivo
        fields = '__all__'
```

## Templates
Vamos criar ``templates/desafio/upload.html`` para fazer upload do arquivo que iremos consumir em nossa API:
```python
{% extends 'base.html' %}
{% load static %}
{% block conteudo %}

<center><a href="http://127.0.0.1:8000/desafio/"><button class="btn btn-primary">API - Consumindo Arquivo</button></a></center>
{%include 'parciais/_messages.html'%}

    <form action="." method="POST" enctype="multipart/form-data">
    {% csrf_token %}
        <div class="mb-3">
            {{ form.as_p }}
        </div>
    <button type="submit" class="btn btn-primary">Enviar</button>
    </form>
{% endblock conteudo %}
```
## Urls
Criaremos o arquivo ``desafio/urls.py``:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```
## Views
Vamos abrir ``desafio/views.py`` no editor de código, apagar tudo dele e escrever o seguinte código:
```python
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

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['nascimento']
    filterset_fields = ['sexo']
```

## Routers
Vamos editar ``core/urls.py`` no editor de código:
```python
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework import routers
from desafio.views import *

router = routers.DefaultRouter()
router.register('mulheres_mereen', MulheresDeMereenViewSet, basename='mulheres_mereen')
router.register('lista_pessoas', ListaDePessoasViewSet, basename='lista_pessoas') 

urlpatterns = [
    path('', include('desafio.urls')),
    path('admin/', admin.site.urls),
    path('desafio/', include(router.urls), name='desafio'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT,
    )
```
## Testando a API
Vamos startar o servidor web
```
python manage.py runserver
```
```
http://127.0.0.1:8000/
```
