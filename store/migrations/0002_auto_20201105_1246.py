# Generated by Django 3.1.2 on 2020-11-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='transaction_id',
            field=models.IntegerField(null=True),
        ),
    ]
