# Generated by Django 5.0.4 on 2025-03-03 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_product_alter_song_title_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='title',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='review',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
