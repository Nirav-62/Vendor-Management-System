# Generated by Django 4.2.7 on 2023-11-30 15:13

import api.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_vendor_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('po_number', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateTimeField(default=api.models.default_delivery_date)),
                ('items', models.JSONField()),
                ('quantity', models.IntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=50)),
                ('quality_rating', models.FloatField(blank=True, null=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('acknowledgment_date', models.DateTimeField(blank=True, null=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.vendor')),
            ],
        ),
    ]
