# Generated by Django 3.2.11 on 2022-05-31 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_business_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='business_logo',
            field=models.ImageField(default='abc.png', upload_to='profile_pic'),
        ),
    ]
