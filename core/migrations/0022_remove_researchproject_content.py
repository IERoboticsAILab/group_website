# Generated by Django 5.2 on 2025-05-25 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0021_alter_jobposition_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="researchproject",
            name="content",
        ),
    ]
