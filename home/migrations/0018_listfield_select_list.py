# Generated by Django 3.1.4 on 2021-01-01 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_listfield_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='listfield',
            name='select_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='select_list', to='home.list'),
        ),
    ]
