# Generated by Django 3.0.7 on 2021-02-11 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quantumforum', '0005_auto_20210204_2339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendships',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
    ]
