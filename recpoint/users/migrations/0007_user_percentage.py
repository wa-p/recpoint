# Generated by Django 2.0.9 on 2018-11-09 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20181004_0437'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='percentage',
            field=models.FloatField(blank=True, default=0, max_length=4, verbose_name='Percentage'),
        ),
    ]
