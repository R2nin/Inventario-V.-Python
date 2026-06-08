from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patrimonio', '0005_xls_referencia_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManutencaoSolicitacao',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_chapa', models.IntegerField(verbose_name='Número da Chapa')),
                ('nome_item',    models.CharField(blank=True, max_length=500, verbose_name='Nome do Item')),
                ('sala',         models.CharField(max_length=255, verbose_name='Sala')),
                ('descricao',    models.TextField(verbose_name='Descrição')),
                ('status',       models.CharField(
                    choices=[('pendente', 'Pendente'), ('concluido', 'Concluído')],
                    default='pendente', max_length=20, verbose_name='Status'
                )),
                ('criado_em',    models.DateTimeField(auto_now_add=True, verbose_name='Solicitado em')),
                ('concluido_em', models.DateTimeField(blank=True, null=True, verbose_name='Concluído em')),
            ],
            options={
                'verbose_name': 'Solicitação de Manutenção',
                'verbose_name_plural': 'Solicitações de Manutenção',
                'ordering': ['-criado_em'],
            },
        ),
    ]
