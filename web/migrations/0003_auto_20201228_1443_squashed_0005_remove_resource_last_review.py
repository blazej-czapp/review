# Generated by Django 3.1.4 on 2020-12-28 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('web', '0003_auto_20201228_1443'), ('web', '0004_resource_next_review'), ('web', '0005_remove_resource_last_review')]

    dependencies = [
        ('web', '0002_auto_20201227_1408'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='last_rep_date',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='rep_count',
        ),
        migrations.AddField(
            model_name='resource',
            name='easiness',
            field=models.FloatField(default=2.36, verbose_name='Easiness'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='interval',
            field=models.IntegerField(default=0, verbose_name='Next review interval'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='repetitions',
            field=models.IntegerField(default=1, verbose_name='Successful review streak'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='resource',
            name='next_review',
            field=models.DateField(default=datetime.date(2020, 12, 28), verbose_name='Next review'),
            preserve_default=False,
        ),
    ]