# Generated by Django 4.2.13 on 2024-07-14 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_addtocart_product_alter_addtocart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=255),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.TextField(max_length=200),
        ),
    ]
