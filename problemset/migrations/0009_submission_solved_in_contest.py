# Generated by Django 4.0.2 on 2022-04-04 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0008_submission_time_solved_in_contest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='solved_in_contest',
            field=models.BooleanField(default=False),
        ),
    ]
