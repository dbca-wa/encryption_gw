# encryption_gw
Central encryption server for encrypting data to be stored in a QR code and used with a mobile device.


This is a test change
```
>>> from encryptiongw import encryption
>>> encr = encryption.encrypt("hello world,  testing 27/02/2023",1)
>>> print (encr)
```

```
>>> encr = encryption.encrypt('{"Name" : "John Blogs", "Expiry": "20/12/2025", "Rego": "1RYMKTR"}',1)
```
