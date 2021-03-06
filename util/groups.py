from .paths import account_path, group_path, get_path
from json import load, dump
import os.path
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
from hashlib import sha256, sha512
from random import choice
from string import ascii_letters, digits, punctuation
from random import shuffle

salt_chars = ascii_letters + digits + punctuation
base64 = ascii_letters + digits + '_-'


def get_groups():
    with open(get_path(group_path)) as f:
        return load(f)


def get_users():
    with open(get_path(account_path)) as f:
        return load(f)


def _hash(s):
    return sha512(s.encode('utf-8')).hexdigest()


def _hash256(s):
    return sha256(s.encode('utf-8')).hexdigest()


def add_group(user, group_name, group_description=''):
    groups = get_groups()
    code = ''.join([choice(base64) for _ in range(16)])
    while code in groups:
        code = ''.join([choice(base64) for _ in range(16)])
    groups[_hash(code)] = {'name': group_name,
                           'users': [user],
                           'description': group_description,
                           'open': True}
    with open(get_path(group_path), 'w') as f:
        dump(groups, f)


def set_expiration(code, expiration):
    groups = get_groups()
    groups[code]['expiration'] = expiration
    with open(get_path(group_path), 'w') as f:
        dump(groups, f)


def _transform(user, data):
    users = get_users()
    key = users[user]['encrypt']
    public = RSA.importKey(key)
    chars = ascii_letters + digits + punctuation
    salt = ''.join([choice(chars) for _ in range(8)])
    data = (data + ' ' + salt).encode('utf-8')
    return hexlify(public.encrypt(data, 32)[0]).decode('utf-8')


def close_group(code):
    # Retrieve groups
    groups = get_groups()
    groups[code]['open'] = False
    users = groups[code]['users'][:]
    # Generate group Santa cycle
    assigned = {}
    start = choice(users)
    user = start
    users.remove(user)
    while users:
        next_user = choice(users)
        assigned[user] = _transform(user, next_user)
        user = next_user
        users.remove(user)
    assigned[user] = _transform(user, start)
    # Reshuffle assignments
    reshuffled = {}
    keys = list(assigned.keys())
    shuffle(keys)
    for key in keys:
        reshuffled[key] = assigned[key]
    assigned = reshuffled
    # Mutate groups and save
    groups[code]['assigned'] = assigned
    with open(get_path(group_path), 'w') as f:
        dump(groups, f)


def join_group(user, code):
    groups = get_groups()
    if _hash(code) not in groups:
        return
    code = _hash(code)
    if groups[code]['open']:
        groups[code]['users'].append(user)
    with open(get_path(group_path), 'w') as f:
        dump(groups, f)


def _decrypt(s, iv, key):
    iv = unhexlify(iv)
    cipher = AES.new(bytes(bytearray.fromhex(key)), AES.MODE_CBC, iv)
    return cipher.decrypt(unhexlify(s)).decode('utf-8')


def _retrieve(user, auth, data):
    users = get_users()
    key = users[user]['decrypt']
    sym_dec = key.split(' ')[0]
    sym_iv = key.split(' ')[1]
    sym_salt = key.split(' ')[2]
    sym_key = _hash256(_hash256(auth + sym_salt) + auth + sym_salt)
    for i in range(1000):
        sym_key = _hash256(sym_key + auth + sym_salt)
    private = RSA.importKey(_decrypt(sym_dec, sym_iv, sym_key))
    result = private.decrypt(unhexlify(data))
    return result


def get_pair(user, auth, code):
    groups = get_groups()
    data = groups[code]['assigned'][user]
    result = _retrieve(user, auth, data)
    return result.decode('utf-8').split(' ')[0]


if __name__ == '__main__':
    from .paths import data_path
    from os import makedirs

    if not os.path.exists(data_path):
        makedirs(data_path)
    with open(get_path(group_path), 'w') as f:
        f.write('{}')
    add_group('Alice', 'A-F')
    groups = get_groups()
    code = None
    for i in groups:
        code = i
    join_group('Bob', code)
    join_group('Charlie', code)
    join_group('Delta', code)
    join_group('Echo', code)
    join_group('Foxtrot', code)
    close_group(code)
    print(get_pair('Alice', 'foo', code))
    print(get_pair('Bob', 'foo', code))
    print(get_pair('Charlie', 'foo', code))
    print(get_pair('Delta', 'bar', code))
    print(get_pair('Echo', 'bar', code))
    print(get_pair('Foxtrot', 'foobar', code))
