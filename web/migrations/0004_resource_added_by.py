# Generated by Django 3.1.4 on 2020-12-29 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('web', '0003_auto_20201228_1443_squashed_0005_remove_resource_last_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='added_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]