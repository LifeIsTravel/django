# Generated by Django 5.1.4 on 2025-01-10 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='extracted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
