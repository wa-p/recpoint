# Generated by Django 2.0.9 on 2018-11-07 22:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shipments', '0027_shipmentpicture_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payed_driver',
        ),
        migrations.RemoveField(
            model_name='shipment',
            name='payed_driver_date',
        ),
        migrations.AddField(
            model_name='shipment',
            name='check_ammount',
            field=models.FloatField(default=0, verbose_name='Check Ammount'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='driver_1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='driver_1', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shipment',
            name='driver_2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='driver_2', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payed_driver_1',
            field=models.BooleanField(default=False, verbose_name='Payed to Driver 1?'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payed_driver_1_date',
            field=models.DateField(blank=True, null=True, verbose_name='Driver 1 Payment Date'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payed_driver_2',
            field=models.BooleanField(default=False, verbose_name='Payed to Driver 2?'),
        ),
        migrations.AddField(
            model_name='shipment',
            name='payed_driver_2_date',
            field=models.DateField(blank=True, null=True, verbose_name='Driver 2 Payment Date'),
        ),
    ]
