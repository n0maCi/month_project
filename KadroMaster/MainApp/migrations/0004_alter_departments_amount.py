# Generated by Django 5.0.6 on 2024-06-02 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_departments_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='amount',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
