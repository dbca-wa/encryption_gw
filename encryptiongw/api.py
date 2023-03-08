from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from encryptiongw import models
from django.utils.crypto import get_random_string
from encryptiongw import models
from encryptiongw import encryption
import json
import datetime
from encryptiongw import models as encryptiongw_models
from encryptiongw import api_utils

@csrf_exempt
def encrypt_data(request, apikey, *args, **kwargs):
    """Encrypt plain text and send back encrypted data with key reference."""
            
    data = request.POST.get('data', '{}')
    group = request.POST.get('group', None)
    print (api_utils.api_allow(api_utils.get_client_ip(request),apikey) )
    if encryptiongw_models.API.objects.filter(api_key=apikey,active=1).count() > 0:
        if api_utils.api_allow(api_utils.get_client_ip(request),apikey) is True:
    
            ek = models.EncryptionKey.objects.filter(group__name=group, active=True)
            if ek.count() > 0:
                encoded_data = encryption.encrypt(data,ek[0].id)
                encrypted_data = "{}|{}".format(ek[0].id,encoded_data.decode('utf-8'))
                
                ed = models.EncryptedData.objects.create(
                    encryption_key=ek[0]               
                )
                
                ed.encrypted_data=str(ed.id)+"|"+encrypted_data
                ed.save()                
                return HttpResponse(json.dumps({'status': 200, 'message': "Success", 'data': ed.encrypted_data}), content_type='application/json', status=200)
        else:            
            return HttpResponse(json.dumps({'status': 403, 'message': "Forbidden Access", 'api_key': apikey, 'ip_address': api_utils.get_client_ip(request)}), content_type='application/json', status=403)
    return HttpResponse(json.dumps({'status': 403, 'message': "Authentication Forbidden", 'ip_address': api_utils.get_client_ip(request)}), content_type='application/json', status=403)


@csrf_exempt
def get_encrypt_data(request, apikey, *args, **kwargs):
    """Encrypt plain text and send back encrypted data with key reference."""
    print (request.POST)
    encrypt_id = request.POST.get('encrypt_id', None)       
    if encryptiongw_models.API.objects.filter(api_key=apikey,active=1).count() > 0:
        print ("KEY")
        if api_utils.api_allow(api_utils.get_client_ip(request),apikey) is True:    
            print ("IP")
            ed = models.EncryptedData.objects.filter(id=encrypt_id)
            if ed.count() > 0:
                return HttpResponse(json.dumps({'status': 200, 'message': "Success", 'data': ed[0].encrypted_data}), content_type='application/json', status=200)
            else:
                return HttpResponse(json.dumps({'status': 200, 'message': "No Data", 'data': ''}), content_type='application/json', status=200)
        else:            
            return HttpResponse(json.dumps({'status': 403, 'message': "Forbidden Access (IP)", 'api_key': apikey, 'ip_address': api_utils.get_client_ip(request)}), content_type='application/json', status=403)
    return HttpResponse(json.dumps({'status': 403, 'message': "Authentication Forbidden (KEY)", 'ip_address': api_utils.get_client_ip(request)}), content_type='application/json', status=403)




@csrf_exempt
def update_device(request, *args, **kwargs):    
    data = request.body
    # React Fetch (mobile app) Seems to send to requests,  a fetch and then a preflight.   
    # First request doesn't have the data only the second request.  
    # If the first request fails then the send request with the data also doesn't get sent.
    device = {}
    if len(data) > 0: 
        got_data = json.loads(data.decode("utf-8"))
        unique_appid = got_data['unique_app_id']
        deviceos = got_data['deviceos']
        app_version = got_data['app_version']
        device_array = models.Device.objects.filter(unique_appid=unique_appid)
        if device_array.count() > 0: 
            device= models.Device.objects.get(id=device_array[0].id)
            device.device_os = deviceos
            device.last_seen = datetime.datetime.now()
            device.app_version = app_version
            device.save()
        else:
            device= models.Device.objects.create(unique_appid=unique_appid)
        rsa_keys = {}
        if device.active is True:            
            device_groups = models.DeviceGroup.objects.filter(device=device)
            
            for dg in device_groups:
                print(dg)
                encryption_keys = models.EncryptionKey.objects.filter(group=dg.group)
                for ek in encryption_keys:
                    rsa_keys['id'+str(ek.id)] =  {"private_key": ek.encryption_private_key}
                    
                
            
        data = {"device": {}, "keys": rsa_keys}
        data['device'] = {'device_id': device.id, "active": device.active}   
   
        response = HttpResponse(json.dumps({'status': 200, 'message': "Success", 'data': data}), content_type='application/json', status=200)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response
    else:
        response = HttpResponse(json.dumps({'status': 200, 'message': "Success", 'data': []}), content_type='application/json', status=200)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "*"
        return response 
    
    
    
    
    
    