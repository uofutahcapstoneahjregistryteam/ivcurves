import argparse
import base64
import csv
import datetime
import json
import requests
import pathlib


TEST_SETS_DIR = 'test_sets'


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def load_overall_scores(filename):
    overall_scores = {}
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            overall_scores[row['test_set']] = row['score']
    return overall_scores


def test_set_filenames():
    return {entry.stem for entry in pathlib.Path(TEST_SETS_DIR).iterdir()
                if entry.is_file()}


def validate_overall_scores(overall_scores):
    valid_test_set_names = test_set_filenames()
    for test_set, score_str in overall_scores.items():
        if test_set not in valid_test_set_names:
            raise ValueError(f'\'{test_set}\' is not a test set')
        float(score_str) # validate is a number


def get_database_sha(github_headers):
    res = requests.get(database_url, headers=github_headers)
    print(res.json())
    return res.json()['sha']


def write_overall_scores_to_database(database, pr_number, pr_author, pr_closed_datetime, overall_scores):
    database[pr_number] = {'username': pr_author,
                           'submission_datetime': pr_closed_datetime,
                           'test_sets': overall_scores}


def push_new_database(database_b64, github_headers):
    database_sha = get_database_sha(github_headers)
    res = requests.put(database_url,
                       headers=github_headers,
                       json={'message':'update database',
                             'committer': {'name':'GitHub',
                                           'email':'github@ivcurves'},
                             'content': f'{database_b64}',
                             'sha': f'{database_sha}'})
    print(res.json())
    res.raise_for_status()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--github-token', dest='github_token', type=str,
                        help='GitHub REST API authentication token')
    parser.add_argument('--pr-author', dest='pr_author', type=str,
                        help='GitHub username of the pull request author')
    parser.add_argument('--pr-number', dest='pr_number', type=int,
                        help='GitHub pull request number')
    parser.add_argument('--pr-closed-at', dest='pr_closed_datetime', type=str,
                        help='Datetime when the GitHub pull request closed')
    parser.add_argument('--repo-owner', dest='repo_owner', type=str,
                        help='GitHub username of the repository\'s owner')
    parser.add_argument('--overall-scores-path', dest='overall_scores_path', type=str,
                        help='Path to the CSV of overall scores')
    parser.add_argument('--database-path', dest='database_path', type=str,
                        help='Path to the JSON scores database')
    args = parser.parse_args()

    database_url = f'https://api.github.com/repos/{args.repo_owner}/ivcurves/contents/{args.database_path}'
    github_headers = {'Accept': 'application/vnd.github+json',
                      'Authorization': f'token {args.github_token}'}

    overall_scores = load_overall_scores(args.overall_scores_path)
    validate_overall_scores(overall_scores)
    database = load_json(args.database_path)
    write_overall_scores_to_database(database, args.pr_number, args.pr_author, args.pr_closed_datetime, overall_scores)

    database_b64 = str(base64.b64encode(json.dumps(database, indent=2).encode('ascii')))[2:-1]
    push_new_database(database_b64, github_headers)

