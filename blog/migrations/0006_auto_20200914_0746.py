# Generated by Django 3.1 on 2020-09-14 02:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_ideathon_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideathon',
            name='Date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
