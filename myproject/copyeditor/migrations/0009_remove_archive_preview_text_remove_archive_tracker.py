# Generated by Django 5.0.1 on 2024-02-05 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copyeditor', '0008_archive_final_text_archive_preview_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archive',
            name='preview_text',
        ),
        migrations.RemoveField(
            model_name='archive',
            name='tracker',
        ),
    ]
