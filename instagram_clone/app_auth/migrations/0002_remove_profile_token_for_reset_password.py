# Generated by Django 3.2.14 on 2022-07-11 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='token_for_reset_password',
        ),
    ]
