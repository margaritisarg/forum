# Generated by Django 4.0.4 on 2022-06-13 13:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_testy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='post',
        ),
    ]
