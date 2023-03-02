from django.contrib import messages
from django.contrib.gis import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.html import format_html
from django.db.models import Q
from encryptiongw import models

@admin.register(models.KeyRegenerate)
class KeyRegenerateAdmin(admin.ModelAdmin):
      list_display = ('id','group','regenerate_days','encryption_bit','next_regenerate_date')
      readonly_fields = ('created',)      
      
@admin.register(models.API)
class APIAdmin(admin.ModelAdmin):
      list_display = ('id','system_name','system_id','active')

@admin.register(models.EncryptionKey)
class EncryptionKey(admin.ModelAdmin):
      list_display = ('id','group','active','created')   
      list_filter = ('group','active')   

@admin.register(models.EncryptedData)
class EncryptedData(admin.ModelAdmin):
      fields = ('encryption_key', 'encrypted_data', 'qrcode_image')
      list_display = ('id','encryption_key','created','qrcode_image')      
      readonly_fields = ('qrcode_image','qrcode','created')
      exclude  = ('qrcode',)
      
      def qrcode_image(self, obj):

            if obj.qrcode:
                 return format_html(                    
                     "<img style='width:200px; height: 200px' src='/private-media/qrcode/"+str(obj.id)+"-file.png'>",
                    )
            else:
                 return format_html(
                     '<b style="font-weight:bold; color: #d72d2d">NO QR CODE</b>',
                    )

class DeviceGroupInline(admin.TabularInline):
    model = models.DeviceGroup
    extra = 0
    raw_id_fields=('group',)

@admin.register(models.Device)
class Device(admin.ModelAdmin):
      list_display = ('id','unique_appid','device_os','app_version','last_seen','expiry_date','active','created')   
      list_filter = ('device_os','active','app_version')   
      inlines = [DeviceGroupInline,]
