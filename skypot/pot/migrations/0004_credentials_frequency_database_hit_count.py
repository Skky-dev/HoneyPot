# Generated by Django 5.1.6 on 2025-02-13 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pot', '0003_credentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentials',
            name='frequency',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='database',
            name='hit_count',
            field=models.IntegerField(default=1),
        ),
    ]
