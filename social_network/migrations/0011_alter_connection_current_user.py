# Generated by Django 4.1.9 on 2023-07-01 08:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network', '0010_remove_connection_connected_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='connection',
            name='current_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
