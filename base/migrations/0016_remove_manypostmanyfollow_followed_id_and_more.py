# Generated by Django 4.0.4 on 2022-06-13 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_follow_post_manypostmanyfollow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manypostmanyfollow',
            name='followed_id',
        ),
        migrations.RemoveField(
            model_name='manypostmanyfollow',
            name='post_id',
        ),
    ]