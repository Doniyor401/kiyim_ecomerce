# Generated by Django 3.2.9 on 2025-02-04 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20250204_0938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='category',
            field=models.CharField(choices=[('Color', 'Color'), ('Size', 'Size'), ('Material', 'Material')], max_length=50),
        ),
    ]
