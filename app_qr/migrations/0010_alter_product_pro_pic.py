# Generated by Django 3.2.11 on 2023-04-16 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_qr', '0009_alter_product_pro_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pro_pic',
            field=models.ImageField(null=True, upload_to='pro_pic'),
        ),
    ]
