# Generated by Django 2.0.4 on 2018-04-17 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0002_auto_20180417_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='hostname',
            field=models.CharField(max_length=64),
        ),
    ]
