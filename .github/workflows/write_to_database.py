import requests
import base64
import json
import argparse


def load_json(filename):
    with open(f'{filename}.json', 'r') as file:
        return json.load(file)


def get_database_sha(GITHUB_HEADERS):
    res = requests.get(DATABASE_URL, headers=GITHUB_HEADERS)
    return res.json()['sha']


def write_scores_to_database(database, scores_json):
    database['test'] = scores_json


def push_new_database(database_b64, GITHUB_HEADERS):
    database_sha = get_database_sha(GITHUB_HEADERS)
    res = requests.put(DATABASE_URL,
                       headers=GITHUB_HEADERS,
                       json={'message':'update database',
                             'committer': {'name':'reepoi',
                                           'email':'reepoi@ivcurves'},
                             'content': f'{database_b64}',
                             'sha': f'{database_sha}'})
    res.raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--github-token', dest='github_token', type=str,
                        help='secrets.GITHUB_TOKEN (or github.token) of the workflow run')
    parser.add_argument('--actor', dest='committer', type=str,
                        help='github.actor of the workflow run')
    cmd_args = parser.parse_args()


    BASE_DIR = '../..'
    DATABASE_URL = 'https://api.github.com/repos/reepoi/ivcurves/contents/database.json'
    GITHUB_TOKEN = cmd_args.github_token
    COMMITTER = cmd_args.committer
    GITHUB_HEADERS = {'Accept': 'application/vnd.github+json',
                      'Authorization': f'token {GITHUB_TOKEN}'}

    database = load_json(f'{BASE_DIR}/database')
    scores_json = load_json('scores.json/scores')
    write_scores_to_database(database, scores_json)

    database_b64 = str(base64.b64encode(json.dumps(database).encode('ascii')))[2:-1]
    push_new_database(database_b64, GITHUB_HEADERS)

