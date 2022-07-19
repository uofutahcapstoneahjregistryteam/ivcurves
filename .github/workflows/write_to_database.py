import sys
import requests
import base64
import json


BASE_DIR = '../..'
DATABASE_URL = 'https://api.github.com/repos/reepoi/ivcurves/contents/database.json'


def load_json(filename):
    with open(f'{BASE_DIR}/{filename}.json', 'r') as file:
        return json.load(file)


def get_database_sha(GITHUB_TOKEN):
    res = requests.get(DATABASE_URL, headers={'Accept': 'application/vnd.github+json',
                               'Authorization': f'token {GITHUB_TOKEN}'})
    return res.json()['sha']


def commit_scores_to_database(database):
    database['test'] = 'hi2'


def push_new_database(database_b64, GITHUB_TOKEN):
    database_sha = get_database_sha(GITHUB_TOKEN)
    res = requests.put(DATABASE_URL,
                       headers={'Accept': 'application/vnd.github+json',
                                'Authorization': f'token {GITHUB_TOKEN}'},
                       data={'message':'update database',
                             'committer': {'name':'reepoi',
                                           'email':'reepoi@ivcurves'},
                             'content': f'{database_b64}',
                             'sha':f'{database_sha}'})
    print(res.json())


assert len(sys.argv) == 2, 'Please pass a GITHUB_TOKEN'

GITHUB_TOKEN = sys.argv[1]

database = load_json('database')
scores = load_json('scores.json/scores')

commit_scores_to_database(database)

database_b64 = str(base64.b64encode(json.dumps(database).encode('ascii')))[2:-1]

push_new_database(database_b64, GITHUB_TOKEN)

