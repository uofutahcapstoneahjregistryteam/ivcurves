import sys
import requests
import base64
import json


def load_json(filename):
    with open(f'{filename}.json', 'r') as file:
        return json.load(file)


def get_database_sha(GITHUB_HEADERS):
    res = requests.get(DATABASE_URL, headers=GITHUB_HEADERS)
    return res.json()['sha']


def write_scores_to_database(database, scores_json):
    database['test'] = scores


def push_new_database(database_b64, database_sha, GITHUB_HEADERS):
    database_sha = get_database_sha(GITHUB_HEADERS)
    res = requests.put(DATABASE_URL,
                       headers=GITHUB_HEADERS,
                       data={'message':'update database',
                             'committer': {'name':'reepoi',
                                           'email':'reepoi@ivcurves'},
                             'content': f'{database_b64}',
                             'sha': f'{database_sha}'})
    print(res.json())


BASE_DIR = '../..'
DATABASE_URL = 'https://api.github.com/repos/reepoi/ivcurves/contents/database.json'
assert len(sys.argv) == 2, 'Please pass a GITHUB_TOKEN'
GITHUB_TOKEN = sys.argv[1]
GITHUB_HEADERS = {'Accept': 'application/vnd.github+json',
                  'Authorization': f'token {GITHUB_TOKEN}'}

database = load_json(f'{BASE_DIR}/database')
scores_json = load_json('scores.json/scores')

write_scores_to_database(database)

database_b64 = str(base64.b64encode(json.dumps(database).encode('ascii')))[2:-1]
push_new_database(database_b64, GITHUB_HEADERS)

