# Generated by Django 3.2.11 on 2023-03-21 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_qr', '0003_auto_20230131_0606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resturant',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
