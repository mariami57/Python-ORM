# Generated by Django 5.0.4 on 2025-03-07 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_menureview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='foodcriticrestaurantreview',
            options={'verbose_name': 'Food Critic Review', 'verbose_name_plural': 'Food Critic Reviews'},
        ),
        migrations.AlterModelOptions(
            name='menureview',
            options={'verbose_name': 'Menu Review', 'verbose_name_plural': 'Menu Reviews'},
        ),
        migrations.AlterModelOptions(
            name='regularrestaurantreview',
            options={'verbose_name': 'Restaurant Review', 'verbose_name_plural': 'Restaurant Reviews'},
        ),
    ]
