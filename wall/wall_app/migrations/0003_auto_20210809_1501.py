# Generated by Django 2.2 on 2021-08-09 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wall_app', '0002_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='user',
            new_name='message_user',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='new_message',
        ),
    ]