# Generated by Django 5.1.3 on 2024-12-03 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
