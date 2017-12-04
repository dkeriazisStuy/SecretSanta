import cgi
import cgitb


def init(debug_cgi=False):
    print('Content-Type: text/html\n')
    print()
    if debug_cgi:
        cgitb.enable()


def render_file(filename):
    with open(filename) as f:
        text = f.read()
    print(text)


def get_fields():
    query = cgi.FieldStorage()
    field_dict = {}
    for i in query.keys():
        field_dict[i] = query[i].value
    return field_dict


def debug(text):
    print('<script type="text/javascript">console.log("' + text + '")</script>')
