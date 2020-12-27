# Generated by Django 3.1.4 on 2020-12-27 18:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0011_record'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type', models.CharField(max_length=200)),
                ('required', models.BooleanField(null=True)),
                ('visible', models.BooleanField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived'), ('deleted', 'Deleted')], default='active', max_length=25)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('list', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.list')),
            ],
        ),
        migrations.CreateModel(
            name='RecordField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('archived', 'Archived'), ('deleted', 'Deleted')], default='active', max_length=25)),
                ('created_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('list_field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.listfield')),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.record')),
            ],
        ),
    ]
