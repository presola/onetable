# Generated by Django 3.1.4 on 2021-02-02 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_recordmedia_name_of_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recordmedia',
            name='name_of_file',
        ),
        migrations.AddField(
            model_name='recordfile',
            name='file_extension',
            field=models.CharField(default='', max_length=200),
        ),
    ]