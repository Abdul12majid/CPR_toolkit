# Generated by Django 5.1.6 on 2025-04-01 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0030_alter_merchant_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='merchant',
            name='amount',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
