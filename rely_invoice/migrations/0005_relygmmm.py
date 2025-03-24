# Generated by Django 5.1.6 on 2025-03-21 19:02

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rely_invoice', '0004_relycompleted_date_paid_relyinvoice_date_paid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelyGMMM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispatch_number', models.CharField(blank=True, max_length=50, null=True)),
                ('customer', models.CharField(blank=True, max_length=50, null=True)),
                ('date_received', models.DateField(default=django.utils.timezone.now)),
                ('date_invoiced', models.DateField(default=django.utils.timezone.now)),
                ('note', models.TextField()),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('date_paid', models.DateField(default=django.utils.timezone.now)),
                ('status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rely_invoice.status')),
            ],
            options={
                'verbose_name_plural': 'Rely GMMM',
            },
        ),
    ]
