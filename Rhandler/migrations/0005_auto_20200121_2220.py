# Generated by Django 3.0.2 on 2020-01-21 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Rhandler', '0004_auto_20200121_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Rhandler.UserInfo'),
        ),
    ]
