from hashlib import sha256, sha512


def hex_hash(s):
    return sha512(s.encode('utf-8')).hexdigest()


def hex_hash256(s):
    return sha256(s.encode('utf-8')).hexdigest()
