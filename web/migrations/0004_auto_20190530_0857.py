# Generated by Django 2.2.1 on 2019-05-30 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_remove_resource_date_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='location_detail',
            new_name='notes',
        ),
    ]
