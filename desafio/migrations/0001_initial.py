# Generated by Django 4.1.4 on 2023-01-16 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadosArquivo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50, verbose_name='Nome:')),
                ('sobrenome', models.CharField(max_length=50, verbose_name='Sobrenome:')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], default='M', max_length=1, verbose_name='Gênero:')),
                ('altura', models.FloatField(verbose_name='Altura:')),
                ('peso', models.FloatField(verbose_name='Peso:')),
                ('nascimento', models.CharField(max_length=50, verbose_name='Data de Nascimento:')),
                ('bairro', models.CharField(max_length=50, verbose_name='Bairro:')),
                ('cidade', models.CharField(max_length=50, verbose_name='Cidade:')),
                ('estado', models.CharField(max_length=50, verbose_name='Estado:')),
                ('numero', models.PositiveIntegerField(verbose_name='Número:')),
            ],
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='')),
            ],
        ),
    ]
