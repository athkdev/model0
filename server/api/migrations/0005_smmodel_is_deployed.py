# Generated by Django 5.1.2 on 2024-10-20 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_smmodel_endpoint_config_name_smmodel_endpoint_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="smmodel",
            name="is_deployed",
            field=models.BooleanField(default=False),
        ),
    ]
