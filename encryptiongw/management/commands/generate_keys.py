from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import Group
import datetime
from encryptiongw import models
from Cryptodome.PublicKey import RSA

class Command(BaseCommand):
    help = 'Remove old logs.'

    def handle(self, *args, **options):
        days_for_deletion = datetime.datetime.now() - datetime.timedelta(days=20)
        #RSAkey = RSA.generate(1024)
        #public_key = RSAkey.publickey().exportKey()
        #private_key = RSAkey.exportKey()
        #print (public_key)
        #print (private_key)
        
        kr = models.KeyRegenerate.objects.filter(next_regenerate_date__lte=datetime.datetime.today())
        for k in kr:
            print (k)
            print ("Generating Keys for group {}".format(k.group.name))
            RSAkey = RSA.generate(k.encryption_bit)
            public_key = RSAkey.publickey().exportKey()
            private_key = RSAkey.exportKey()
            #print (public_key)
            #print (private_key)
            next_generate_date = datetime.datetime.now() + datetime.timedelta(days=k.regenerate_days)
            #print (next_generate_date.date())
            
            models.EncryptionKey.objects.create(
                group=k.group,
                encryption_private_key=private_key.decode('utf-8'),
                encryption_public_key=public_key.decode('utf-8'),
                active=True,                                                                      
            )
            
            k.next_regenerate_date=next_generate_date.date()   
            k.save()

