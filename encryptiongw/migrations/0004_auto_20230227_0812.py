# Generated by Django 3.2.18 on 2023-02-27 08:12

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('encryptiongw', '0003_encrypteddata_qrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='encryptionkey',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='encrypteddata',
            name='qrcode',
            field=models.FileField(blank=True, max_length=512, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/private-media/', location='/data/data/projects/encryption_gw/private-media/'), upload_to='qrcode/'),
        ),
    ]
