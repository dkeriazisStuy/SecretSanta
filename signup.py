#!/usr/bin/env python3
import render
from util import add_user, remember

render.init(True)


def main():
    fields = render.get_fields()
    try:
        username = fields['username']
        email = fields['email']
        key = fields['key']
        nonce = fields['nonce']
    except KeyError:
        return render.redirect('error.html')
    add_user(username, email, key, nonce)
    if 'series_id' in fields and 'token' in fields:
        series_id = fields['series_id']
        token = fields['token']
        remember(username, series_id, token)
    render.redirect('home.html')


main()
