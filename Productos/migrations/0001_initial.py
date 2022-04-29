# Generated by Django 3.2.12 on 2022-04-28 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=30)),
                ('tipo_producto', models.CharField(max_length=20)),
                ('precio_producto', models.IntegerField(default=0)),
                ('modo_venta', models.CharField(max_length=30)),
                ('stock_producto', models.IntegerField(default=0)),
                ('descripcion_producto', models.TextField(max_length=350)),
                ('imagen_producto', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
