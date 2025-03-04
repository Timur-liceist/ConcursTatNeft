# Generated by Django 5.1.6 on 2025-03-03 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название события')),
            ],
        ),
        migrations.CreateModel(
            name='EventModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100, verbose_name='дата')),
                ('content', models.TextField(verbose_name='событие')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.historymodel', verbose_name='событие')),
            ],
            options={
                'verbose_name': 'событие',
                'verbose_name_plural': 'события',
            },
        ),
    ]
