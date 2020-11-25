# Generated by Django 3.0.7 on 2020-11-25 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0003_blogcontributorapplication'),
    ]

    operations = [
        migrations.RenameField(
            model_name='credential',
            old_name='quantum_session',
            new_name='session',
        ),
        migrations.AddField(
            model_name='credential',
            name='session_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
