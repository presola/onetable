# Generated by Django 3.1.4 on 2020-12-22 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_app_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='fields',
            field=models.JSONField(),
        ),
    ]