#!/usr/bin/env python3
import render
from util import add_user

render.init()


def main():
    fields = render.get_fields()
    try:
        username = fields['username']
        email = fields['email']
        key = fields['key']
        nonce = fields['nonce']
    except KeyError:
        return  # TODO: Render "something went wrong" page
    print(key, '<br>')
    print(nonce, '<br><br>')
    add_user(username, email, key, nonce)
    # print("Account created")


main()
