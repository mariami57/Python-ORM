# Generated by Django 5.0.4 on 2025-03-22 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_article_authors_alter_review_article_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='published_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
