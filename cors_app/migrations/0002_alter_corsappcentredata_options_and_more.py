# Generated by Django 5.0.4 on 2024-04-29 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cors_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='corsappcentredata',
            options={'managed': False},
        ),
        migrations.AlterField(
            model_name='vendor_data',
            name='offset_parameter_of_antenna',
            field=models.FileField(blank=True, null=True, upload_to='image/'),
        ),
    ]