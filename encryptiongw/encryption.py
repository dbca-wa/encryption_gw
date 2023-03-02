from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP, PKCS1_v1_5
import base64
from base64 import b64encode, b64decode
from encryptiongw import models
import time
#time.clock = time.time

def get_keys(key_id):
    ek = models.EncryptionKey.objects.filter(id=key_id)
    pub_key = RSA.importKey(ek[0].encryption_public_key)
    key = RSA.importKey(ek[0].encryption_private_key)
    return key, pub_key

def encrypt(data,key_id):
    private, public = get_keys(key_id)  
    encryptor = PKCS1_v1_5.new(public)
    encrypted = encryptor.encrypt(data.encode("utf-8"))
    encrypted_encoded = base64.b64encode(encrypted)
    return encrypted_encoded
    
def decrypt(encrypted_encoded_data,key_id):
    private, public = get_keys(key_id)
    decryptor = PKCS1_v1_5.new(private)
    decoded_encrypted = base64.b64decode(encrypted_encoded_data)
    decoded_decypted = decryptor.decrypt(decoded_encrypted)
    return decoded_decypted.decode("utf-8")
    
   