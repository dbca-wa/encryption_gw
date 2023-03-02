from django.http import HttpResponse, HttpResponseRedirect
from encryptiongw import models
import os 
import mimetypes

def getAppFile(request,file_id,extension):
    allow_access = False
    #if request.user.is_superuser:
 
    if request.user.is_staff is True:
        allow_access = True
  
    if allow_access == True:
        file_data = models.EncryptedData.objects.get(id=file_id)
        file_name_path = file_data.qrcode.path
        if os.path.isfile(file_name_path) is True:
                the_file = open(file_name_path, 'rb')
                the_data = the_file.read()
                the_file.close()
                if extension == 'msg': 
                    return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
                if extension == 'eml':
                    return HttpResponse(the_data, content_type="application/vnd.ms-outlook")


                return HttpResponse(the_data, content_type=mimetypes.types_map['.'+str(extension)])
    else:
                return HttpResponse("Error loading attachment", content_type="plain/html")
                