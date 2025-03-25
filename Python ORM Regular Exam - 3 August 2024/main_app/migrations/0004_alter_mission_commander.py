# Generated by Django 5.0.4 on 2025-03-25 14:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_astronaut_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mission',
            name='commander',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commanded_missions', to='main_app.astronaut'),
        ),
    ]
