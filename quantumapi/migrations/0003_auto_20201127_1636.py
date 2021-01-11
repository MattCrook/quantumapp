# Generated by Django 3.0.7 on 2020-11-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0002_auto_20201127_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credential',
            name='access_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='audience',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='client_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='csrf_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='django_token',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='nonce',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='redirect_uri',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='scope',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='session',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='session_id',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='transactions',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='credential',
            name='user_sub',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]