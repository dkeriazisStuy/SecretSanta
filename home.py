#!/usr/bin/env python3
import render
from util import remember

render.init()


def main():
    render.render_file("home.html")
    fields = render.get_fields()
    if 'series_id' in fields and 'token' in fields and 'username' in fields:
        series_id = fields['series_id']
        token = fields['token']
        username = fields['username']
        remember(username, series_id, token)


main()
