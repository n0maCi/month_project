# Generated by Django 5.0.6 on 2024-06-05 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_jobs_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='access',
        ),
        migrations.AddField(
            model_name='user',
            name='access_lvl',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.DeleteModel(
            name='Accesses',
        ),
    ]
