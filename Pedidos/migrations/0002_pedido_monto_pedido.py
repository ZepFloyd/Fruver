# Generated by Django 3.2.12 on 2022-04-19 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Pedidos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='monto_pedido',
            field=models.IntegerField(default=0),
        ),
    ]