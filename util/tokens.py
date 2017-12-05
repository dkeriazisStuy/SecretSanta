from util import salt_chars, token_path, get_path, hex_hash
from random import choice

from json import load


def get_tokens():
    with open(get_path(token_path)) as f:
        return load(f)


def remember(username, series_id, token):
    tokens = get_tokens()
    tokens[series_id] = {'token': hex_hash(token), 'username': username}


def check_remember(username, series_id, token):
    tokens = get_tokens()
    if series_id in tokens:
        if tokens[series_id] == hex_hash(token):
            token = ''.join([choice(salt_chars) for _ in range(16)])
            remember(username, series_id, token)
            return True
        else:
            return False  # TODO: Implement warnings and cool-down for forged token
    return False
