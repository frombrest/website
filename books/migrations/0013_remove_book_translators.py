# Generated by Django 3.2.19 on 2023-11-06 03:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0012_auto_20231105_0604"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="translators",
        ),
    ]
