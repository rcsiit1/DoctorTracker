# Generated by Django 2.1.5 on 2019-07-25 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorfinder', '0002_payments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='customer_id',
            field=models.CharField(max_length=300),
        ),
    ]