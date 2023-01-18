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



