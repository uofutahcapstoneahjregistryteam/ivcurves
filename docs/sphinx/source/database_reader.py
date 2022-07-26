import datetime
import json
from mpmath import mp


def load_scores_database():
    with open('../../../scores_database.json', 'r') as file:
        return json.load(file)


def to_ghuser(username):
    return f':ghuser:`{username}`'


def to_pull(pr_number):
    return f':pull:`{pr_number}`'


def date_from_github_datetime_str(ghdatetime_str):
    ghdatetime = datetime.datetime.strptime(ghdatetime_str, '%Y-%m-%dT%H:%M:%SZ')
    return ghdatetime.strftime('%m/%d/%Y')


def leaderboard_entry_list():
    database = load_scores_database()
    processed_data = []

    for pr_number, submission_data in database.items():
        processed_data.append({
            'pr_number': to_pull(pr_number),
            'username': to_ghuser(submission_data['username']),
            'overall_score': sum(mp.mpmathify(v) for v in submission_data['test_sets'].values()),
            'submission_date': date_from_github_datetime_str(submission_data['submission_datetime'])
        })

    processed_data.sort(key=lambda l: l['overall_score'])

    for idx, entry in enumerate(processed_data):
        entry['Index'] = f'#{idx + 1}'
        entry['overall_score'] = mp.nstr(entry['overall_score'])

    return processed_data

