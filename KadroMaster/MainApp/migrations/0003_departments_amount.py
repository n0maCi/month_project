# Generated by Django 5.0.6 on 2024-06-02 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_accesses_departments_remove_user_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='departments',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]
