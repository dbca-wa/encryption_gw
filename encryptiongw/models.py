from __future__ import unicode_literals
from datetime import timedelta
from django.conf import settings
from django.contrib.gis.db import models
#from django.contrib.postgres.fields import JSONField
from django.urls import reverse
#from model_utils import Choices
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
from encrypted_model_fields.fields import EncryptedCharField
from datetime import datetime
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
import qrcode
import os

private_storage = FileSystemStorage(location=str(settings.BASE_DIR)+"/private-media/", base_url='/private-media/')

today = datetime.now()
today_path = today.strftime("%Y/%m/%d/%H")

class EncryptionKey(models.Model):
        encryption_private_key = models.TextField(null=True, blank=True, default='')
        encryption_public_key = models.TextField(null=True, blank=True, default='')
        group = models.ForeignKey(Group, blank=True, null=True, related_name='group', on_delete=models.SET_NULL)
        active = models.BooleanField(default=True)
        created = models.DateTimeField(auto_now_add=True)
        
        def save(self, *args, **kwargs):
            # set all other keys active=False if this key active=True
            if self.active is True:
                EncryptionKey.objects.filter(group=self.group,active=True).update(active=False)            
            super(EncryptionKey, self).save(*args,**kwargs)
        
        def __str__(self):
            return '{}'.format(str(self.id)) 

def store_qr_code(instance, filename):
    return '{}/qrcode/'.format(settings.BASE_DIR, instance.id)

class EncryptedData(models.Model):
        encryption_key = models.ForeignKey(EncryptionKey, blank=True, null=True, related_name='encryption_key_id', on_delete=models.SET_NULL)
        encrypted_data = models.TextField(null=True, blank=True, default='')
        qrcode = models.FileField(upload_to="qrcode/", null=True, max_length=512,  storage=private_storage, blank=True)
        created = models.DateTimeField(auto_now_add=True)
        
        def save(self, *args, **kwargs):
                if len(self.encrypted_data) > 0:                         
                        img = qrcode.make(self.encrypted_data)
                        img.save("/tmp/tmp_qrcode-{}.png".format(str(self.id)))
                        destination_file = open("/tmp/tmp_qrcode-{}.png".format(str(self.id)), 'rb')
                        self.qrcode.save('qrcode-{}.png'.format(str(self.id)), File(destination_file), save=False)
                        destination_file.close()
                        os.remove("/tmp/tmp_qrcode-{}.png".format(str(self.id)))                                   
                super(EncryptedData, self).save(*args,**kwargs)
                
        def __str__(self):
                return "{}".format(str(self.id))


class API(models.Model):
    STATUS = (
       (0, 'Inactive'),
       (1, 'Active'),
    )

    system_name = models.CharField(max_length=512)
    system_id = models.CharField(max_length=4, null=True, blank=True)
    api_key = models.CharField(max_length=512,null=True, blank=True, default='', help_text="Key is auto generated,  Leave blank or blank out to create a new key")
    allowed_ips = models.TextField(null=True, blank=True, default='', help_text="Use network ranges format: eg 1 ip = 10.1.1.1/32 or for a c class block of ips use 192.168.1.0/24 etc")
    active = models.SmallIntegerField(choices=STATUS, default=0) 

    def save(self, *args, **kwargs):
        if self.api_key is not None:

             if len(self.api_key) > 1:
                  pass
             else:
                  self.api_key = self.get_random_key(100)
        else:
            self.api_key = self.get_random_key(100)
        super(API,self).save(*args,**kwargs)


    def get_random_key(self,key_length=100):
        return get_random_string(length=key_length, allowed_chars=u'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')        
    
class KeyRegenerate(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True, related_name='key_regenerate_group', on_delete=models.SET_NULL)
    encryption_bit = models.IntegerField(help_text="", default=2048)
    regenerate_days = models.IntegerField(help_text="", default=1)
    next_regenerate_date = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} days, next regenerate date {}".format(str(self.regenerate_days), self.next_regenerate_date)
    
    def save(self, *args, **kwargs):    
        if self.next_regenerate_date is None:
            self.next_regenerate_date = datetime.today()
        super(KeyRegenerate, self).save(*args,**kwargs)
        
    def clean(self, *args, **kwargs):    
        kr = KeyRegenerate.objects.filter(group=self.group).exclude(id=self.id)
        if kr.count() > 0: 
            raise ValidationError('A key regeneration rule already exists for group {} '.format(self.group.name))                
        if self.encryption_bit < 1024:
            raise ValidationError('Encryption bit too small {} '.format(self.encryption_bit))                
        #super(KeyRegenerate, self).save(*args,**kwargs)
        

class Device(models.Model):
    unique_appid = models.CharField(max_length=512)
    device_os = models.CharField(max_length=50)
    app_version = models.CharField(max_length=50, default='')
    expiry_date = models.DateTimeField(null=True, blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{}".format(str(self.unique_appid))

class DeviceGroup(models.Model):
    device = models.ForeignKey(Device, blank=True, null=True, related_name='device_group_device', on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, blank=True, null=True, related_name='device_group_group', on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}".format(str(self.group.name))