# Generated by Django 5.1.6 on 2025-02-21 17:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0007_alter_invoice_created_at_alter_journal_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
