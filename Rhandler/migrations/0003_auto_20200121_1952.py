# Generated by Django 3.0.2 on 2020-01-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rhandler', '0002_userinfo_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=24),
        ),
    ]
