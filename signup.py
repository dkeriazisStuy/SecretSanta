#!/usr/bin/env python3
# import render
import cgi


def make_dict(field):
    field_dict = {}
    for i in field.keys():
        field_dict[i] = field[i].value
    return field_dict


# render.init()
# render.render_file('signup.html')
print(make_dict(cgi.FieldStorage))
