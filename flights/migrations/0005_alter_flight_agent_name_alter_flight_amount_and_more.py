# Generated by Django 5.1.4 on 2025-01-10 03:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("flights", "0004_alter_flight_table"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="agent_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="amount",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="flight",
            name="url",
            field=models.TextField(null=True),
        ),
    ]
