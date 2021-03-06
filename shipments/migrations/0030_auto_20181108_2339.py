# Generated by Django 2.0.9 on 2018-11-08 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0029_auto_20181108_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cost',
            name='ammount',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payed_ammount',
        ),
        migrations.RemoveField(
            model_name='paymentvariation',
            name='ammount',
        ),
        migrations.RemoveField(
            model_name='pricehistory',
            name='ammount',
        ),
        migrations.AddField(
            model_name='cost',
            name='amount',
            field=models.FloatField(default=0, max_length=15, verbose_name='Amount'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payed_amount',
            field=models.FloatField(default=0, max_length=15, verbose_name='Payed Amount'),
        ),
        migrations.AddField(
            model_name='paymentvariation',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Variation Amount'),
        ),
        migrations.AddField(
            model_name='pricehistory',
            name='amount',
            field=models.FloatField(default=0, max_length=15, verbose_name='Amount'),
        ),
    ]
