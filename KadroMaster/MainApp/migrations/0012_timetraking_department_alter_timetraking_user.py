# Generated by Django 5.0.6 on 2024-06-06 15:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0011_user_password_kadr'),
    ]

    operations = [
        migrations.AddField(
            model_name='timetraking',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.jobs'),
        ),
        migrations.AlterField(
            model_name='timetraking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.departments'),
        ),
    ]