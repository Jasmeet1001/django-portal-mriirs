# Generated by Django 4.1 on 2022-12-08 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_additionalinfo_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='dept',
            field=models.CharField(blank=True, max_length=7),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='h_index',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='i_index',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
