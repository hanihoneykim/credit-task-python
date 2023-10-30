# Generated by Django 4.2.6 on 2023-10-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50)),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("stationery", "문구류"),
                            ("digital", "디지털"),
                            ("character", "캐릭터"),
                            ("living", "리빙"),
                            ("pet", "반려동물"),
                        ],
                        max_length=15,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Categories",
            },
        ),
    ]
