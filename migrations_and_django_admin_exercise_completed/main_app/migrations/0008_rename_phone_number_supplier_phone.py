# Generated by Django 5.0.4 on 2025-02-20 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_course_supplier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='phone_number',
            new_name='phone',
        ),
    ]
