# Generated by Django 3.2.18 on 2023-02-27 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encryptiongw', '0004_auto_20230227_0812'),
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.CharField(max_length=512)),
                ('system_id', models.CharField(blank=True, max_length=4, null=True)),
                ('api_key', models.CharField(blank=True, default='', help_text='Key is auto generated,  Leave blank or blank out to create a new key', max_length=512, null=True)),
                ('allowed_ips', models.TextField(blank=True, default='', help_text='Use network ranges format: eg 1 ip = 10.1.1.1/32 or for a c class block of ips use 192.168.1.0/24 etc', null=True)),
                ('active', models.SmallIntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0)),
            ],
        ),
    ]