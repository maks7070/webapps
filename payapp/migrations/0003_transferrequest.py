# Generated by Django 5.0.3 on 2024-03-28 00:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payapp', '0002_alter_transaction_recipient_alter_transaction_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_payer', to='payapp.wallet')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_requestor', to='payapp.wallet')),
            ],
        ),
    ]
