# Generated by Django 3.0.7 on 2021-02-08 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0034_applogindata'),
    ]

    operations = [
        migrations.AddField(
            model_name='applogindata',
            name='strategy',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='applogindata',
            name='strategy_type',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
