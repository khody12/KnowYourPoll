# Generated by Django 4.2.14 on 2024-08-17 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_poll_aggregate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll_aggregate',
            name='date',
            field=models.DateField(),
        ),
    ]
