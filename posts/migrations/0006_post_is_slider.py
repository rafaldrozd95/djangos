# Generated by Django 3.1.3 on 2020-11-27 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20201126_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_slider',
            field=models.BooleanField(default=False),
        ),
    ]
