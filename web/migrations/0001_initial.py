# Generated by Django 2.2.1 on 2019-05-30 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.TextField()),
                ('rep_count', models.IntegerField(default=0, verbose_name='Times repeated')),
                ('last_rep_date', models.DateField(verbose_name='Last repetition')),
                ('location', models.TextField(help_text='e.g. URL or book title')),
                ('notes', models.TextField(help_text='e.g. section title or book page number')),
            ],
        ),
    ]
