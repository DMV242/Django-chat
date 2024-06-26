# Generated by Django 5.0.3 on 2024-04-05 13:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_room_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(error_messages={'unique': 'Une room avec  ce nom existe déjà.'}, max_length=100, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_champ', message='Le nom ne doit contenir que des lettres et des chiffres.', regex='^[a-zA-Z0-9]+$')]),
        ),
    ]
