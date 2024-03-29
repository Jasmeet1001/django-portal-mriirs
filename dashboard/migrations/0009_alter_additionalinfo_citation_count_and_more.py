# Generated by Django 4.1 on 2022-10-30 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_rename_desgignation_additionalinfo_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalinfo',
            name='citation_count',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='dept',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='designation',
            field=models.CharField(default='', max_length=4),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='h_index',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='i_index',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='month_year',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='orcid_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='scopus_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='vidwan_id',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='additionalinfo',
            name='wos_id',
            field=models.CharField(default='', max_length=50),
        ),
    ]
