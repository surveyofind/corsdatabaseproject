# Generated by Django 5.0.4 on 2024-04-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cors_app', '0002_alter_corsappcentredata_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor_data',
            name='operationmaintainanceremark',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterModelTable(
            name='corsappcentredata',
            table='cors_app_centre_data',
        ),
    ]
