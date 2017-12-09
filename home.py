#!/usr/bin/env python3
import render
from util import remember, add_group, add_user, get_groups

render.init(True)


def call(func):
    try:
        func()
    except KeyError:
        pass


def main():
    fields = render.get_fields()

    try:
        username = fields['username']
    except KeyError:
        return render.redirect('error.html')

    call(lambda: add_user(username, fields['email'], fields['key'], fields['nonce']))
    call(lambda: remember(username, fields['series_id'], fields['series_token']))
    call(lambda: add_group(username, fields['group_name'], fields['group_description']))

    group_str = '<ul>'
    groups = get_groups()
    for code in get_groups():
        if username in groups[code]['users']:
            group_str += '<li>'
            group_str += groups[code]['name']
            group_str += '</li>'
    group_str += '</ul>'

    render.render_file("home.html", username=username, groups=group_str)


main()
