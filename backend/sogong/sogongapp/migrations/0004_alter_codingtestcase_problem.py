# Generated by Django 4.1.7 on 2023-06-01 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sogongapp", "0003_remove_ethicssubmission_problem_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="codingtestcase",
            name="problem",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
