# Generated by Django 3.2.11 on 2023-04-16 10:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20230416_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='activation_key_forget_password',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_password_forget',
        ),
    ]
