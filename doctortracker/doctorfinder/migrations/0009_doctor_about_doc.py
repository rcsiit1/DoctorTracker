# Generated by Django 2.1 on 2019-04-19 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctorfinder', '0008_auto_20190419_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='about_doc',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]