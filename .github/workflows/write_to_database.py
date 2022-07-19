import sys
import base64
import json


BASE_DIR = '../..'


def load_json(filename):
    with open(f'{BASE_DIR}/{filename}.json', 'r') as file:
        return json.load(file)


assert len(sys.argv) == 2, 'Please pass a GITHUB_TOKEN'

GITHUB_TOKEN = sys.argv[1]

database = load_json('database')
scores = load_json('scores.json/scores')

database['test'] = 'hi'

database_base64 = str(base64.b64encode(json.dumps(database).encode('ascii')))[2:-1]

bash_cmd_update_database = (
'curl '
'-X PUT '
'-H "Accept: application/vnd.github+json" '
f'-H "Authorization: token {GITHUB_TOKEN}" '
'https://api.github.com/repos/reepoi/ivcurves/contents/database.json '
).replace('"', '\'')
bash_cmd_update_database += \
    f'-d \'{{"message":"update database","committer":{{"name":"reepoi","email":"reepoi@ivcurves"}},"content":"{database_base64}"}}\''
print(bash_cmd_update_database)

