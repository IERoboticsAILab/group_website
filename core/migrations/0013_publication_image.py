# Generated by Django 5.2 on 2025-05-18 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0012_remove_publication_authors_from_team_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="publication",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="publications/"),
        ),
    ]
