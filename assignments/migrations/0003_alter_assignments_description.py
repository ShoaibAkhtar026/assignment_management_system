# Generated by Django 3.2.12 on 2022-03-29 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignments', '0002_auto_20220329_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]