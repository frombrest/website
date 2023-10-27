# Generated by Django 3.2.19 on 2023-10-27 04:27

import books.models
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_narration_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='narration',
            name='cover_image',
            field=models.ImageField(blank=True, null=True, upload_to=functools.partial(books.models._get_image_name, *('covers',), **{})),
        ),
        migrations.AddField(
            model_name='narration',
            name='date',
            field=models.DateField(null=True, verbose_name='Release Date'),
        ),
        migrations.AddField(
            model_name='narration',
            name='translators',
            field=models.ManyToManyField(blank=True, related_name='narrations_translated', to='books.Person'),
        ),
    ]
