# Generated by Django 5.1.6 on 2025-03-06 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0017_alter_ebay_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebay',
            name='tracking_number',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
