# Generated by Django 5.1.6 on 2025-03-24 16:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rely_invoice', '0005_relygmmm'),
    ]

    operations = [
        migrations.CreateModel(
            name='Work_Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatch_number', models.CharField(blank=True, max_length=50, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('date_received', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
