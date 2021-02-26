# Generated by Django 3.0.7 on 2021-02-24 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0041_credential_codes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='credential',
            options={'get_latest_by': 'updated_at', 'verbose_name': 'credential', 'verbose_name_plural': 'credentials'},
        ),
        migrations.AddField(
            model_name='loginhistory',
            name='user_logs',
            field=models.TextField(blank=True, null=True),
        ),
    ]