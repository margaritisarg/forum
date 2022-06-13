# Generated by Django 4.0.4 on 2022-06-13 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_remove_post_follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='follow',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.follow'),
            preserve_default=False,
        ),
    ]