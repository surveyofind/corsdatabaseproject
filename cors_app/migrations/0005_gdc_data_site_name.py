# Generated by Django 5.0.4 on 2024-04-30 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cors_app', '0004_vendor_data_site_name_vendor_data_state_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gdc_data',
            name='site_name',
            field=models.TextField(blank=True, null=True),
        ),
    ]
