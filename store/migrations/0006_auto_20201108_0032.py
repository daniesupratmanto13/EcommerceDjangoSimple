# Generated by Django 3.1.2 on 2020-11-08 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_productmodel_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitemmodel',
            old_name='pruduct',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='image',
            field=models.ImageField(blank=True, default='placeholder.jpg', null=True, upload_to=''),
        ),
    ]
