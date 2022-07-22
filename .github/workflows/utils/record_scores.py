import argparse
import csv
import json
import requests
import pathlib


TEST_SETS_DIR = '../../test_sets'


def load_json(filename):
    with open(f'{filename}.json', 'r') as file:
        return json.load(file)


def load_overall_scores(filename)
    overall_scores = {}
    with open(f'{filename}.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            overall_scores[row['test_set']] = row['score']
    return overall_scores


def test_set_filenames():
    return {entry.name for entry in pathlib.Path(TEST_SETS_DIR).iterdir()
                if entry.is_file()}


def validate_overall_scores(overall_scores):
    valid_test_set_names = test_set_filenames()
    for test_set, score_str in overall_scores:
        if row['test_set'] not in valid_test_set_names():
            raise ValueError('\'{test_set}\' is not a test set')
        float(row['score']) # validate is a number


def get_database_sha(GITHUB_HEADERS):
    res = requests.get(DATABASE_URL, headers=GITHUB_HEADERS)
    return res.json()['sha']


def write_overall_scores_to_database(database, pr_number, overall_scores):
    database[pr_number] = overall_scores


def push_new_database(database_b64, GITHUB_HEADERS):
    database_sha = get_database_sha(GITHUB_HEADERS)
    res = requests.put(DATABASE_URL,
                       headers=GITHUB_HEADERS,
                       json={'message':'update database',
                             'committer': {'name':'GitHub',
                                           'email':'github@ivcurves'},
                             'content': f'{database_b64}',
                             'sha': f'{database_sha}'})
    res.raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--github-token', dest='github_token', type=str,
                        help='GitHub REST API authentication token')
    parser.add_argument('--pr-number', dest='pr_number', type=int,
                        help='GitHub pull request number')
    parser.add_argument('--repo-owner', dest='repo_owner', type=str,
                        help='GitHub username of the repository\'s owner')
    parser.add_argument('--database-path', dest='database_path', type=str,
                        help='Path to the JSON scores database')
    args = parser.parse_args()

    relative_database_path = pathlib.Path(args.database_path)

    # Assumes database is in the root directory of the repository
    database_url = f'https://api.github.com/repos/{args.repo_owner}/ivcurves/contents/{relative_database_path.name}'
    github_headers = {'Accept': 'application/vnd.github+json',
                      'Authorization': f'token {args.github_token}'}

    overall_scores = load_overall_scores('overall_scores.csv/overall_scores')
    validate_overall_scores(overall_scores)
    database = load_json(args.database)
    write_overall_scores_to_database(database, args.pr_number, overall_scores)

    database_b64 = str(base64.b64encode(json.dumps(database).encode('ascii')))[2:-1]
    push_new_database(database_b64, GITHUB_HEADERS)

