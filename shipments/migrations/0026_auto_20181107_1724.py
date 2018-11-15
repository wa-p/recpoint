# Generated by Django 2.0.9 on 2018-11-07 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0025_paymentvariation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipmentPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, max_length=200, null=True, upload_to='')),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shipments.Shipment')),
            ],
        ),
        migrations.AlterField(
            model_name='paymentvariation',
            name='ammount',
            field=models.FloatField(verbose_name='Variation Ammount'),
        ),
    ]
