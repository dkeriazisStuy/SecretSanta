#!/usr/bin/env python3
import render
from util import join_group, hex_hash

render.init()


def main():
    fields = render.get_fields()
    if 'id' in fields and 'user' in fields:
        join_group(fields['user'], fields['id'])
        render.redirect('home.py')
    else:
        render.redirect('index.html')


main()
