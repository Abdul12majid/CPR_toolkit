# Generated by Django 5.1.6 on 2025-04-04 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0034_amex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amex',
            old_name='delivery_time',
            new_name='transaction_date',
        ),
    ]
