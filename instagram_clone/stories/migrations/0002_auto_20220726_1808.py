# Generated by Django 3.2.14 on 2022-07-26 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
        migrations.RenameField(
            model_name='story',
            old_name='date',
            new_name='posted',
        ),
    ]