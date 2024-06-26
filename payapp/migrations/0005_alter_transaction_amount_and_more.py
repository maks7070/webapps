# Generated by Django 5.0.3 on 2024-04-24 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0004_wallet_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='transferrequest',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.FloatField(default=1000),
        ),
    ]
