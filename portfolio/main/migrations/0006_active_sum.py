# Generated by Django 3.2 on 2021-05-26 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_active_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='active',
            name='sum',
            field=models.FloatField(default=0, null=True, verbose_name='Сумма'),
        ),
    ]
