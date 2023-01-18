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

