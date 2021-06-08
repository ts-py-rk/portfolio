# Generated by Django 3.2 on 2021-05-26 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210526_2013'),
    ]

    operations = [
        migrations.AddField(
            model_name='active',
            name='quantity',
            field=models.FloatField(default=0, null=True, verbose_name='Количество'),
        ),
        migrations.AddField(
            model_name='active',
            name='rate',
            field=models.FloatField(default=0, null=True, verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='active',
            name='pozition',
            field=models.CharField(choices=[('лонг', 'Long'), ('шорт', 'Short')], default='лонг', max_length=5, verbose_name='Тип позиции'),
        ),
        migrations.AlterField(
            model_name='active',
            name='price',
            field=models.FloatField(default=0, null=True, verbose_name='Цена'),
        ),
    ]
