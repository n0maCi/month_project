# Generated by Django 5.0.6 on 2024-06-06 15:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0012_timetraking_department_alter_timetraking_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timetraking',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='MainApp.departments'),
        ),
        migrations.AlterField(
            model_name='timetraking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]