#!/usr/bin/env python3
import render
from util import remember

render.init(True)


def main():
    # render.render_file("home.html")
    fields = render.get_fields()
    render.debug(str(fields))
    if 'series_id' in fields and 'series_token' in fields and 'username' in fields:
        series_id = fields['series_id']
        series_token = fields['series_token']
        username = fields['username']
        remember(username, series_id, series_token)
        render.debug("New token generated")


main()
