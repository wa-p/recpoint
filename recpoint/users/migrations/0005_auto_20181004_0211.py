# Generated by Django 2.0.9 on 2018-10-04 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20181004_0006'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='actual_picture',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='actual_pic'),
        ),
        migrations.AddField(
            model_name='user',
            name='licence_picture',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='licence_pic'),
        ),
    ]