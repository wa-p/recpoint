# Generated by Django 2.0.9 on 2018-10-16 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0017_auto_20181016_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentCompany',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Company Name')),
            ],
        ),
    ]
