# Generated by Django 3.1.4 on 2020-12-20 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_list_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='description',
            field=models.TextField(default='Lorem ipsum this is an awesome organization'),
            preserve_default=False,
        ),
    ]