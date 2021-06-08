# Generated by Django 3.2 on 2021-05-29 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_active_sum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='active',
            name='sum',
        ),
        migrations.AlterField(
            model_name='active',
            name='pozition',
            field=models.CharField(choices=[('лонг', 'купил'), ('шорт', 'продал')], default='лонг', max_length=5, verbose_name='Тип позиции'),
        ),
    ]
