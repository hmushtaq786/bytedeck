# Generated by Django 2.2.12 on 2020-05-30 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0009_auto_20200530_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siteconfig',
            name='banner_image',
            field=models.ImageField(blank=True, help_text='The banner will be displayed on your landing page and in a smaller format at the top left of the site (up to 1140px wide)', null=True, upload_to='', verbose_name='Banner Image'),
        ),
    ]
