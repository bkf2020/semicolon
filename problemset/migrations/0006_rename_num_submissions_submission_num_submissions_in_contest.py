# Generated by Django 4.0.2 on 2022-02-24 00:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0005_remove_submission_user_answer_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='num_submissions',
            new_name='num_submissions_in_contest',
        ),
    ]
