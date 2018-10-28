# Generated by Django 2.0.9 on 2018-10-16 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0019_auto_20181016_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='provider_company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='shipments.ShipmentCompany'),
        ),
    ]