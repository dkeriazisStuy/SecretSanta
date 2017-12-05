from os.path import dirname, realpath, join

data_path = '../data/'
account_path = '../data/accounts.json'
group_path = '../data/groups.json'
token_path = '../data/tokens.json'


def get_path(path):
    return join(dirname(realpath(__file__)), path)
