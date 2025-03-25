# Generated by Django 5.0.4 on 2025-03-24 18:07

import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='astronaut',
            name='phone_number',
            field=models.CharField(max_length=15, unique=True, validators=[main_app.validators.DigitsOnlyValidator()]),
        ),
    ]
