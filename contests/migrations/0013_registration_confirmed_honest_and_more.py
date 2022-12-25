# Generated by Django 4.1.4 on 2022-12-25 04:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0012_contest_contest_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='confirmed_honest',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='registration',
            name='verify_end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]