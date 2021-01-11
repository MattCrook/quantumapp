# Generated by Django 3.0.7 on 2020-12-11 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0016_calendarevent'),
    ]

    operations = [
        migrations.AddField(
            model_name='calendarevent',
            name='is_reminder_set',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='calendarevent',
            name='reminder_value',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]