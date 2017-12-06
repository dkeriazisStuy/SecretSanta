from .users import salt_chars, get_users
from .hash import hex_hash
from .paths import account_path, get_path
from random import choice

from json import dump


def remember(username, series_id, series_token):
    users = get_users()
    users[username]['series_id'] = series_id
    users[username]['series_token'] = hex_hash(series_token)
    # print(hex_hash(series_token))
    with open(get_path(account_path), 'w') as f:
        dump(users, f)


def check_remember(series_id, series_token):
    users = get_users()
    for user in users:
        if user['series_id'] == series_id:
            if user['series_token'] == hex_hash(series_token):
                new_token = ''.join(choice(salt_chars) for _ in range(16))
                remember(user, series_id, new_token)
                return True
            else:
                return False  # TODO: Implement warnings and cool-down for forged token
    return False
