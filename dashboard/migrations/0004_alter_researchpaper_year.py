# Generated by Django 4.1 on 2022-10-24 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_researchpaper_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchpaper',
            name='year',
            field=models.IntegerField(blank=True),
        ),
    ]
