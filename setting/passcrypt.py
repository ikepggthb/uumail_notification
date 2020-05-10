# uumail notification
#
# © 2020 Ikkei Yamada All Rights Reserved.
# Twitter: @idkaeti
# Email  : ikeprg@gmail.com

#   Released under the GPLv3 license.
#
#   "uumail_notification" is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#   "uumail_notification" is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#   You should have received a copy of the GNU General Public License
#   along with "uumail_notification".  If not, see <http://www.gnu.org/licenses/>.

from getpass import getpass
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from os.path import expanduser
import os
import sys

PATH_DIR = expanduser("~") + '\\AppData\\Roaming\\uumail_notification\\account'
PATH_PASSWD = PATH_DIR + '\\login.data'
PATH_KEY = PATH_DIR + '\\login.key'
PATH_ID = PATH_DIR+"\\loginid.txt"


def read_bin(path):
    with open(path, mode = "rb") as f:
	    data = f.read()
    return data

def write_bin(path, data):
    with open(path, mode = "wb") as f:
	    f.write(data)

def encrypt(input_data):   # str型平文  -->  バイナリ（key,暗号化データ）
    passwd = pad(input_data.encode("utf-8"), AES.block_size)
    key  = Random.get_random_bytes(AES.block_size)
    iv   = Random.get_random_bytes(AES.block_size)
    encrypt_obj = AES.new(key, AES.MODE_CBC, iv)
    data_enc = encrypt_obj.encrypt(passwd)
    return {'key':key, 'passwd':iv + data_enc}

def decrypt(key, input_data):  # バイナリ（key,暗号化データ） -->  str型平文
    # ivと暗号化データに分ける
    iv   = input_data[0:AES.block_size]
    data_enc = input_data[AES.block_size :]
    # 復号化オブジェクトを生成
    decrypt_obj = AES.new(key, AES.MODE_CBC, iv=iv)
    # 復号化、バイナリをstrに変換
    data = unpad(decrypt_obj.decrypt(data_enc), AES.block_size).decode('utf-8')
    return data

def read_data():
    data = read_bin(PATH_PASSWD)
    key = read_bin(PATH_KEY)
    passwd = decrypt(key, data)
    with open(PATH_ID, mode='r') as f:
        loginid = f.read()
    return loginid, passwd

def write_data(loginid,passwd):
    erc = encrypt(passwd)
    write_bin(PATH_KEY, erc['key'])
    write_bin(PATH_PASSWD, erc['passwd'])
    with open(PATH_ID, mode='w') as f:
        f.write(loginid)

os.makedirs(PATH_DIR, exist_ok=True)




