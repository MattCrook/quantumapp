# Generated by Django 3.0.7 on 2020-11-29 22:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quantumapi', '0012_auto_20201129_2203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loginhistory',
            old_name='app_code_name',
            new_name='appcodename',
        ),
        migrations.RenameField(
            model_name='loginhistory',
            old_name='host_computer_name',
            new_name='hostcomputername',
        ),
        migrations.RenameField(
            model_name='loginhistory',
            old_name='ip_address',
            new_name='ipaddress',
        ),
        migrations.RenameField(
            model_name='loginhistory',
            old_name='recent_attempts',
            new_name='recentattempts',
        ),
        migrations.RenameField(
            model_name='loginhistory',
            old_name='total_logins',
            new_name='totallogins',
        ),
    ]
