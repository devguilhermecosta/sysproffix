# Generated by Django 5.0.4 on 2024-04-11 19:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospital',
            name='stock',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='stock.stock'),
        ),
    ]
