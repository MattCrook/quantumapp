# Generated by Django 3.0.7 on 2021-02-08 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0037_auto_20210208_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='applogindata',
            name='prompts',
            field=models.TextField(blank=True, null=True),
        ),
    ]
