# Generated by Django 3.0.6 on 2020-06-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0003_auto_20200601_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='timestamp',
            field=models.DateField(null=True),
        ),
    ]
