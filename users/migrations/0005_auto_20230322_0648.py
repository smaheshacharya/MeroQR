# Generated by Django 3.2.11 on 2023-03-22 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_is_active'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneOTP',
        ),
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
    ]