# Generated by Django 4.0.2 on 2022-02-23 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problemset', '0002_problem_visible'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='correct_answer',
            field=models.IntegerField(default=0),
        ),
    ]