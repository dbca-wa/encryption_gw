# Generated by Django 3.2.18 on 2023-03-01 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryptiongw', '0010_device_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='app_version',
            field=models.CharField(default='', max_length=50),
        ),
    ]