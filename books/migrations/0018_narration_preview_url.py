# Generated by Django 5.0.1 on 2024-01-28 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0017_auto_20231231_0602"),
    ]

    operations = [
        migrations.AddField(
            model_name="narration",
            name="preview_url",
            field=models.CharField(
                blank=True, default="", max_length=100, verbose_name="Preview URL"
            ),
        ),
    ]
