# Generated by Django 3.2.12 on 2022-04-25 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Productos', '0002_producto_imagen_producto'),
        ('Pedidos', '0005_auto_20220424_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio_producto', models.IntegerField(default=0)),
                ('modo_venta', models.CharField(max_length=30, null=True)),
                ('cantidad_producto', models.IntegerField(default=0)),
                ('subtotal', models.IntegerField(default=0)),
                ('id_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Pedidos.pedido')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Productos.producto')),
            ],
        ),
        migrations.AddField(
            model_name='pedido',
            name='detalle_pedido',
            field=models.ManyToManyField(through='Pedidos.DetallePedido', to='Productos.Producto'),
        ),
    ]