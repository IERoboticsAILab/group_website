# Generated by Django 5.2 on 2025-05-18 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_teammember_position"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchproject",
            name="banner_image",
            field=models.ImageField(
                blank=True,
                help_text="Banner image for the project",
                null=True,
                upload_to="projects/banners/",
            ),
        ),
        migrations.AddField(
            model_name="researchproject",
            name="publications",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="core.publication"
            ),
        ),
        migrations.AddField(
            model_name="researchproject",
            name="team_members",
            field=models.ManyToManyField(
                blank=True, related_name="projects", to="core.teammember"
            ),
        ),
        migrations.CreateModel(
            name="ProjectGalleryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("image", models.ImageField(upload_to="projects/gallery/")),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="core.researchproject",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project Gallery Image",
                "verbose_name_plural": "Project Gallery Images",
                "ordering": ["order"],
            },
        ),
    ]
