import argparse
import csv
import json
import pathlib


ROOT_DIR = pathlib.Path(f'{__file__}/../../..').resolve()
TEST_SETS_DIR = pathlib.Path(f'{ROOT_DIR}/test_sets')


def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def save_json(json_dict, filename):
    with open(filename, 'w') as file:
        return json.dump(json_dict, file, indent=2)


def load_overall_scores(filename):
    overall_scores = {}
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            overall_scores[row['test_set']] = row['score']
    return overall_scores


def test_set_filenames():
    return {entry.stem for entry in TEST_SETS_DIR.iterdir() if entry.is_file()}


def validate_overall_scores(overall_scores):
    valid_test_set_names = test_set_filenames()
    for test_set, score_str in overall_scores.items():
        if test_set not in valid_test_set_names:
            raise ValueError(f'\'{test_set}\' is not a test set')
        float(score_str) # validate is a number


def write_overall_scores_to_database(database, pr_number, pr_author, pr_closed_datetime, overall_scores):
    database[pr_number] = {'username': pr_author,
                           'submission_datetime': pr_closed_datetime,
                           'test_sets': overall_scores}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr-author', dest='pr_author', type=str,
                        help='GitHub username of the pull request author')
    parser.add_argument('--pr-number', dest='pr_number', type=int,
                        help='GitHub pull request number')
    parser.add_argument('--pr-closed-at', dest='pr_closed_datetime', type=str,
                        help='Datetime when the GitHub pull request closed')
    parser.add_argument('--overall-scores-path', dest='overall_scores_path', type=str,
                        help='Path to the CSV of overall scores')
    parser.add_argument('--database-path', dest='database_path', type=str,
                        help='Path to the JSON scores database')
    args = parser.parse_args()

    overall_scores = load_overall_scores(args.overall_scores_path)
    validate_overall_scores(overall_scores)
    database = load_json(args.database_path)
    write_overall_scores_to_database(database, args.pr_number, args.pr_author, args.pr_closed_datetime, overall_scores)
    save_json(database, f'{ROOT_DIR}/{args.database_path}')

