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
