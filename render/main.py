import cgi
import cgitb


def init(debug=False):
    print('Content-Type: text/html\n')
    print()
    if debug:
        cgitb.enable()


def render_file(filename):
    with open(filename) as f:
        text = f.read()
    print(text)


def make_dict(field):
    field_dict = {}
    for i in field.keys():
        field_dict[i] = field[i].value
    return field_dict


def debug(text):
    print('<script type="text/javascript">console.log("' + text + '")</script>')
