# Generated by Django 2.2.12 on 2020-04-18 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteconfig', '0006_auto_20200403_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteconfig',
            name='access_code',
            field=models.CharField(default='314159', help_text='Students will need this to sign up to your deck.  You can set it to any string of characters you like.', max_length=128, verbose_name='Access Code'),
        ),
    ]
