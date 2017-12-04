def init():
    print('Content-Type: text/html\n')
    print()


def render_file(filename):
    with open(filename) as f:
        text = f.read()
    print(text)
