# Generated by Django 2.2.5 on 2020-03-04 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_auto_20200303_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
