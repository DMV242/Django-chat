# Generated by Django 5.0.3 on 2024-04-05 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_message_image_alter_message_content'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='Image',
            new_name='image',
        ),
    ]