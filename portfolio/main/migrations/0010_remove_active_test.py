# Generated by Django 3.2 on 2021-05-30 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_active_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='active',
            name='test',
        ),
    ]