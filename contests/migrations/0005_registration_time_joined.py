# Generated by Django 4.0.2 on 2022-03-07 01:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0004_contest_time_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='time_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]