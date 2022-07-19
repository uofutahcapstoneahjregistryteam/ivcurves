import os
import re
import csv
import json


BASE_DIR = '../..'
SCORE_PATH = f'scores.json/scores.json'
TESTS_DIR = f'{BASE_DIR}/tests'


def case_filenames():
    """
    Returns a sorted list of filenames in the directory `TESTS_DIR`.
    The filenames do not have file extensions.

    Returns
    -------
    set 
        A set of filenames without file extensions.
    """
    res = set()
    for _, _, filenames in os.walk(TESTS_DIR):
        for filename in filenames:
            res.add(filename.split(".")[0])
    return res


def load_scores():
    with open(SCORE_PATH, 'r') as score_file:
        return json.load(score_file)


def load_case_indices(case_filename):
    with open(f'{TESTS_DIR}/{name}.csv', 'r') as case_parameter_sets_file:
        reader = csv.DictReader(case_parameter_sets_file, delimiter=',')
        indices = set()
        for row in reader:
            indices.add(row['Index'])
        return indices


score_json = load_scores()
case_names = case_filenames()

if case_names != set(score_json.keys()):
    error_msg = f'Unknown case names: {", ".join(set(score_json.keys()) - case_names)}'
    raise ValueError(error_msg)

for name in case_names:
    indices = load_case_indices(name)

    if indices != set(score_json[name].keys()):
        error_msg = f'Unknown case test indices: {", ".join(set(score_json[name].keys()) - indices)}'
        raise ValueError(error_msg)

    score_re = re.compile('^[0-9]+\.[0-9]+$')
    bad_score_values = [score for score in score_json[name].values() if not re.match(score_re, score)]

    if bad_score_values:
        error_msg = f'Invalid score values: {", ".join(bad_score_values)}'
        raise ValueError(error_msg)

