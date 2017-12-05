from .paths import account_path
from json import load, dump
import os.path
from os.path import realpath, dirname
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
import binascii
from hashlib import sha256, sha512
from random import choice
from string import ascii_letters, digits, punctuation

salt_chars = ascii_letters + digits + punctuation


def get_path(path):
    return os.path.join(dirname(realpath(__file__)), path)


def get_users():
    with open(get_path(account_path)) as f:
        return load(f)


def _hash(s):
    return sha512(s.encode('utf-8')).hexdigest()


def get_hash(s, salt):
    result = _hash(_hash(s + salt) + s + salt)
    for i in range(1000):
        result = _hash(result + s + salt)
    return result + ' ' + salt


def _hash256(s):
    return sha256(s.encode('utf-8')).hexdigest()


def _encrypt(s, key):
    iv = Random.get_random_bytes(16)
    cipher = AES.new(bytes(bytearray.fromhex(key)), AES.MODE_CBC, iv)
    return (binascii.hexlify(cipher.encrypt(s)) + b' ' + binascii.hexlify(iv)).decode('utf-8')


def _extend(key, num):
    return key + ' ' * (num - len(key) % num)


def add_user(username, email, auth, nonce=''):
    if user_exists(username) or email_exists(email):
        return
    users = get_users()
    salt = ''.join([choice(salt_chars) for _ in range(8)])
    # Add user keys
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    public = key.publickey().exportKey().decode('utf-8')
    private = key.exportKey().decode('utf-8')
    sym_salt = ''.join([choice(salt_chars) for _ in range(8)])
    sym_key = _hash256(_hash256(auth + sym_salt) + auth + sym_salt)
    for i in range(1000):
        sym_key = _hash256(sym_key + auth + sym_salt)
    private = _extend(private, 16)
    enc = _encrypt(private, sym_key)
    # Modify users
    users[username] = {'pass': get_hash(_hash(auth + nonce), salt),
                       'nonce': nonce,
                       'email': email,
                       'encrypt': public,
                       'decrypt': enc + ' ' + sym_salt}
    # Write new users
    with open(get_path(account_path), 'w') as f:
        dump(users, f)


def check_user(username, auth):
    users = get_users()
    check = users[username]['pass']
    salt = check.split(' ')[1]
    nonce = users[username]['nonce']
    result = get_hash(_hash(auth + nonce), salt)
    # Check to protect from length extension attacks
    if len(check) != len(result):
        return False
    equality = True
    for i in range(len(check)):
        if check[i] != result[i]:
            equality = False
    return equality


def user_exists(user):
    return user in get_users()


def email_exists(email):
    users = get_users()
    for user in users:
        if users[user]['email'] == email:
            return True
    return False


def delete_user(user):
    users = get_users()
    del users[user]
    with open(get_path(account_path), 'w') as f:
        dump(users, f)


def change_password(username, auth, new_pass):
    if not check_user(username, auth):
        return False
    users = get_users()
    salt = ''.join([choice(salt_chars) for _ in range(8)])
    users[username]['pass'] = get_hash(new_pass, salt)
    with open(get_path(account_path), 'w') as f:
        dump(users, f)
    return True


if __name__ == '__main__':
    from .paths import data_path
    from os import makedirs

    if not os.path.exists(data_path):
        makedirs(data_path)
    with open(get_path(account_path), 'w') as f:
        f.write('{}')
    add_user('Alice', 'alice@example.com', 'foo')
    add_user('Bob', 'bob@example.com', 'foo')
    add_user('Charlie', 'charlie@example.com', 'foo')
    add_user('Delta', 'delta@example.com', 'bar')
    add_user('Echo', 'echo@example.com', 'bar')
    add_user('Foxtrot', 'foxtrot@example.com', 'foobar')
    add_user('Golf', 'golf@example.com', 'baz')
    print(email_exists('golf@example.com'))
    delete_user('Golf')
    print(email_exists('golf@example.com'))
    print(check_user('Alice', 'Foo'))
    print(check_user('Alice', 'foo'))
    print(check_user('Bob', 'Foo'))
    print(check_user('Bob', 'foo'))
    print(change_password('Alice', 'foo', 'FooBar'))
    print(change_password('Alice', 'foo', 'Blah'))
    print(check_user('Alice', 'FooBar'))
