from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from os.path import expanduser


def read_bin(path):
    with open(path, mode = "rb") as f:
	    data = f.read()
    return data

def write_bin(path, data):
    with open(path, mode = "wb") as f:
	    f.write(data)

def encrypt(input_data):   # str型平文  -->  バイナリ（key,暗号化データ）
    data = pad(input_data.encode("utf-8"), AES.block_size)
    key  = Random.get_random_bytes(16)
    iv   = Random.get_random_bytes(AES.block_size)
    encrypt_obj = AES.new(key, AES.MODE_CBC, iv)
    data_enc = encrypt_obj.encrypt(data)
    return key, iv + data_enc

def decrypt(key, input_data):  # バイナリ（key,暗号化データ） -->  str型平文
    iv   = input_data[0:16]
    data_enc = input_data[16:]
    decrypt_obj = AES.new(key, AES.MODE_CBC, iv = iv)
    data = unpad(decrypt_obj.decrypt(data_enc), AES.block_size).decode('utf-8')
    return data

def read_data():
    data_path = expanduser("~") + '\\AppData\\Local\\uumail_notification\\account'
    data = read_bin(data_path + '\\login.data')
    key = read_bin('settings\\login.key')
    passwd = decrypt(key, data)
    with open(data_path+"\\loginid.txt", mode='r') as f:
        loginid = f.read()
    return loginid, passwd





