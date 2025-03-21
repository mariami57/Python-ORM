# Generated by Django 5.0.4 on 2025-03-17 06:52

import main_app.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogame',
            name='rating',
            field=models.DecimalField(decimal_places=1, max_digits=2, validators=[main_app.validators.RangeValidator(max_value=Decimal('10'), message='The rating must be between 0.0 and 10.0', min_value=Decimal('0'))]),
        ),
        migrations.AlterField(
            model_name='videogame',
            name='release_year',
            field=models.PositiveIntegerField(validators=[main_app.validators.RangeValidator(max_value=2023, message='The release year must be between 1990 and 2023', min_value=1990)]),
        ),
    ]
