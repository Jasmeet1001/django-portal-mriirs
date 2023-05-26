# Generated by Django 4.1.6 on 2023-05-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_profile_is_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchpaper',
            name='authors',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='domain',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='name_of_conference',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='name_of_journal',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='outside_authors',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='title_of_book',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='title_of_chapter',
            field=models.CharField(blank=True, max_length=400),
        ),
        migrations.AlterField(
            model_name='researchpaper',
            name='title_of_paper',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
