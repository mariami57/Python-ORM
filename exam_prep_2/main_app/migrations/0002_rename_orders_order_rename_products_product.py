# Generated by Django 5.0.4 on 2025-03-20 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]
