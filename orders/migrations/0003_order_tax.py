# Generated by Django 4.0.5 on 2022-07-09 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_first_name_order_name_remove_order_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
