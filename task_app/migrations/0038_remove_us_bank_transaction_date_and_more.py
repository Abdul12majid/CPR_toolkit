# Generated by Django 5.1.6 on 2025-04-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0037_us_bank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='us_bank',
            name='transaction_date',
        ),
        migrations.AddField(
            model_name='us_bank',
            name='transaction_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
