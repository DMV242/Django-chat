# Generated by Django 5.0.3 on 2024-04-01 00:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]