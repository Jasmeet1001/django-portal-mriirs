# Generated by Django 4.1 on 2022-12-07 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_remove_researchpaper_affilation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='researchpaper',
            name='student',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]