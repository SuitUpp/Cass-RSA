import socket
import rsa
from base64 import b64encode, b64decode

client = socket.socket()
client.connect(('localhost',5051))


choice = input('Choose any one.\n1.Encrption Decryption.\n2.Digital Signature.\n3.Both.\n4.Quit\n').encode()
client.send(choice)
#receive public key
public = rsa.importKey(client.recv(1024))
private = rsa.importKey(client.recv(1024))
if int(choice) == 1:
    print('Encyption Decryption')
    while True:
        #send encryption message
        msg = input('Enter message:').encode()
        encrypted = b64encode(rsa.encrypt(msg, public))
        client.send(encrypted)
        msge = client.recv(1024)
        if msge == b'Quit':
            client.close()
            break 
        else:
            # encrypted = client.recv(1024)
            print(rsa.decrypt(b64decode(msge), private))
        # if rsa.decrypt(b64decode(encrypted), private) == b'Quit':
        #     client.close()
        #     break 
elif int(choice) == 2:
    print('Digital Signature')
    msg = client.recv(1024)
    ##Accepting signature
    sign = client.recv(1024)
    #Verify signature
    verify = rsa.verify(msg, b64decode(sign), public)
    print('Is the Sender Verified ?', verify)
    client.close()

elif int(choice) == 3:
    print('Encryption Decryption With Digital Signature')
    msg = client.recv(1024)
    ##Accepting signature
    sign = client.recv(1024)
    #Verify signature
    verify = rsa.verify(msg, b64decode(sign), public)
    print('Is the Sender Verified ?', verify)
    #client.send(b'True' if verify else b'False')
    if verify:
        # msg = input('Enter message:').encode()
        # encrypted = b64encode(rsa.encrypt(msg, public))
        # client.send(encrypted)
        while True:
        #send encryption message
            msg = input('Enter message:').encode()
            encrypted = b64encode(rsa.encrypt(msg, public))
            client.send(encrypted)
            msge = client.recv(1024)
            if msge == b'Quit':
                client.close()
                break 
            else:
                # encrypted = client.recv(1024)
                print(rsa.decrypt(b64decode(msge), private)) 
    else:
        print('User Is not verified')
        client.close()
    