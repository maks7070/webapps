# Generated by Django 5.0.3 on 2024-04-26 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0005_alter_transaction_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferrequest',
            name='completed',
            field=models.CharField(default='no', max_length=100),
        ),
    ]
