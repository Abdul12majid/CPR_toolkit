# Generated by Django 5.1.6 on 2025-03-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0013_alter_invoice_invoiced_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='days_difference',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
