# Generated by Django 5.1.4 on 2025-01-10 02:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("flights", "0003_remove_flight_id_alter_flight_extracted_at_and_more"),
    ]

    operations = [
        migrations.AlterModelTable(
            name="flight",
            table="flight",
        ),
    ]
