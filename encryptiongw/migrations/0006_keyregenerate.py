# Generated by Django 3.2.18 on 2023-02-28 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('encryptiongw', '0005_api'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyRegenerate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regenerate_days', models.IntegerField(default=1)),
                ('next_regenerate_date', models.DateField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='key_regenerate_group', to='auth.group')),
            ],
        ),
    ]
