# Generated by Django 3.1.3 on 2020-12-06 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20201206_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofilemodel',
            name='image',
            field=models.ImageField(blank=True, default='users/annonymous.png', null=True, upload_to='users/'),
        ),
    ]
